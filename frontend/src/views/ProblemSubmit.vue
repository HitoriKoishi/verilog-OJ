<script setup>
// 添加导入
import SubmitHistory from '../components/SubmitHistory.vue';
import { ref, onMounted, onUnmounted } from 'vue';
import message from '../utils/message';
import { useRoute } from 'vue-router';
import { problemApi, submissionApi, aiApi } from '../api';
import CollapsibleSection from '../components/CollapsibleSection.vue';
import MarkdownRenderer from '../components/MarkdownRenderer.vue';
import VerilogEditor from '../components/VerilogEditor.vue';
import LogViewer from '../components/LogViewer.vue';
import WaveformViewer from '../components/WaveformViewer.vue';
import { marked } from 'marked';

const route = useRoute();
const problemId = route.params.id;

const problem = ref(null);
const loading = ref(true);
const error = ref(null);
const verilogCode = ref('');
const editorRef = ref(null);
const historyRef = ref(null);

// 获取单个题目的详细信息
const fetchProblemDetail = async () => {
    loading.value = true;
    error.value = null;

    try {
        const response = await problemApi.getProblem(problemId);

        if (response.status !== 200) {
            throw new Error(`服务器返回错误状态码: ${response.status}`);
        }

        if (!response.data) {
            throw new Error('服务器返回数据为空');
        }

        problem.value = {
            id: response.data.id,
            title: response.data.title,
            description: response.data.document,
            difficulty: response.data.difficulty,
            tags: response.data.tags,
            codeTemplate: response.data.code_template
        };

        if (response.data.code_template && !verilogCode.value) {
            verilogCode.value = response.data.code_template;
        }

        console.log('成功获取题目数据:', problem.value);
    } catch (err) {
        console.error('获取题目详情失败:', err);
        error.value = err.response?.data?.message || err.message || '获取题目详情失败';
    } finally {
        loading.value = false;
    }
};

// 添加一个新的动画控制函数
const toggleSections = async () => {
    descriptionExpanded.value = false;
    await new Promise(resolve => setTimeout(resolve, 300));
    logExpanded.value = true;
    waveformExpanded.value = true;
};

// 提交解答
const submitSolution = async () => {
    if (!verilogCode.value.trim()) {
        message.warning('请输入Verilog代码');
        return;
    }

    logSectionStatus.value = 'default';

    try {
        aiAnalysisResult.value = '';
        showAiAnalysis.value = false;

        const submitResponse = await problemApi.submitSolution(problemId, verilogCode.value);

        if (!submitResponse.data || !submitResponse.data.submission_id) {
            throw new Error('提交失败: 服务器返回无效的提交ID');
        }

        currentSubmissionId.value = submitResponse.data.submission_id;
        message.success('代码提交成功，正在评测...');

        await toggleSections();

        setTimeout(() => {
            checkSubmissionResult(currentSubmissionId.value);
        }, 1000);

        if (historyRef.value) {
            historyRef.value.refresh();
        }

    } catch (err) {
        console.error('提交解答失败:', err);
        message.error('提交失败: ' + (err.response?.data?.error || err.message || '未知错误'));
    }
};

// 轮询检查提交结果
const checkSubmissionResult = async (submissionId) => {
    try {
        const resultResponse = await submissionApi.getSubmission(submissionId);
        const submissionData = resultResponse.data;

        if (submissionData.status === 'queued' || submissionData.status === 'running') {
            setTimeout(() => {
                checkSubmissionResult(submissionId);
            }, 3000);
            return;
        }

        await fetchLogAndWaveform(submissionId);

        if (submissionData.status === 'success') {
            logSectionStatus.value = 'success';
            message.success('提交成功！您的代码已通过测试');
        } else {
            logSectionStatus.value = 'error';
            message.error(`提交失败: ${submissionData.error_code}`);
        }
    } catch (err) {
        console.error('获取提交结果失败:', err);
        logSectionStatus.value = 'error';
        message.error('获取提交结果失败: ' + (err.response?.data?.error || err.message || '未知错误'));
    }
};

// 保存代码草稿
const saveDraft = async () => {
    if (!verilogCode.value.trim()) {
        message.info('草稿为空');
        return;
    }
    try {
        const response = await problemApi.saveDraft(problemId, verilogCode.value);
        if (response.status === 200) {
            message.success('代码草稿已保存');
        }
    } catch (err) {
        console.error('保存代码草稿失败:', err);
        message.error(err.response?.data?.error || '保存代码草稿失败');
    }
};

// 加载代码草稿
const loadDraft = async () => {
    try {
        const response = await problemApi.loadDraft(problemId);

        if (response.status === 200) {
            if (response.data.draft_code) {
                verilogCode.value = response.data.draft_code;
                updateEditorContent(response.data.draft_code);
                if (response.data.draft_time) {
                    message.info(`已加载代码草稿，保存时间: ${response.data.draft_time}`);
                }
                return true;
            } else {
                message.info('没有找到保存的代码草稿');
                return false;
            }
        }
    } catch (err) {
        console.error('加载代码草稿失败:', err);
        message.error(err.response?.data?.error || '加载代码草稿失败');
        return false;
    }
};

// 更新编辑器内容的方法
const updateEditorContent = (code) => {
    if (editorRef.value) {
        editorRef.value.updateContent(code);
    }
};

// 清空编辑器内容
const clearEditor = () => {
    verilogCode.value = '';
    if (editorRef.value) {
        editorRef.value.clearContent();
    }
};

onMounted(async () => {
    console.log('组件挂载');
    await fetchProblemDetail();
    await loadDraft();
});

let autoSaveInterval;
onMounted(() => {
    autoSaveInterval = setInterval(saveDraft, 60000);
});

onUnmounted(() => {
    clearInterval(autoSaveInterval);
});

// 添加控制变量
const descriptionExpanded = ref(true);
const logExpanded = ref(false);
const waveformExpanded = ref(false);
const currentLog = ref('');
const currentWaveform = ref('');
const currentSubmissionId = ref(null);

// 获取日志和波形的函数
const fetchLogAndWaveform = async (submissionId) => {
    try {
        const logResponse = await submissionApi.getSubmissionLog(submissionId);
        if (logResponse.status === 200) {
            currentLog.value = logResponse.data.log_content;
        }

        const waveformResponse = await submissionApi.getSubmissionWaveform(submissionId);
        if (waveformResponse.status === 200) {
            currentWaveform.value = waveformResponse.data.waveform_content;
        }
    } catch (err) {
        console.error('获取日志或波形失败:', err);
        message.error(err.response?.data?.error || '获取日志或波形失败');
    }
};

// 添加日志状态控制
const logSectionStatus = ref('default');

// 处理历史记录选择
const handleHistorySelect = async (submissionId) => {
  try {
    // 打开日志和波形面板
    toggleSections();
    
    // 获取并显示日志和波形
    await fetchLogAndWaveform(submissionId);
    
    // 设置当前提交ID
    currentSubmissionId.value = submissionId;
    
    // 获取提交状态并更新日志状态
    const resultResponse = await submissionApi.getSubmission(submissionId);
    const submissionData = resultResponse.data;
    
    // 更新日志状态颜色
    logSectionStatus.value = submissionData.status === 'success' ? 'success' : 'error';
    
  } catch (err) {
    console.error('获取历史提交详情失败:', err);
    message.error('获取历史提交详情失败: ' + (err.response?.data?.error || err.message || '未知错误'));
  }
};

// 添加AI分析相关的状态
const isAnalyzing = ref(false);
const aiAnalysisResult = ref('');
const showAiAnalysis = ref(false);
const isAnalysisEntering = ref(false);

// 获取AI分析
const getAiAnalysis = async () => {
    if (!currentSubmissionId.value) {
        message.warning('请先提交代码');
        return;
    }

    try {
        isAnalyzing.value = true;
        showAiAnalysis.value = false;
        message.info('正在请求AI分析，请稍候...');

        const response = await aiApi.getAnalysis(currentSubmissionId.value);

        if (response.data && response.data.analysis) {
            // 先隐藏旧的分析结果
            await new Promise(resolve => {
                if (showAiAnalysis.value) {
                    showAiAnalysis.value = false;
                    setTimeout(resolve, 300); // 等待淡出动画完成
                } else {
                    resolve();
                }
            });

            aiAnalysisResult.value = response.data.analysis;
            isAnalysisEntering.value = true;
            showAiAnalysis.value = true;
            
            // 触发进入动画
            setTimeout(() => {
                isAnalysisEntering.value = false;
                message.success('AI分析完成');
            }, 50);
        } else {
            throw new Error('分析结果为空');
        }
    } catch (err) {
        console.error('获取AI分析失败:', err);
        message.error('获取AI分析失败: ' + (err.response?.data?.error || err.message || '未知错误'));
        aiAnalysisResult.value = '获取分析失败: ' + (err.response?.data?.error || err.message || '未知错误');
        showAiAnalysis.value = false;
    } finally {
        isAnalyzing.value = false;
    }
};
</script>

<template>
    <div class="problem-submit container">
        <div v-if="loading" class="loading-container">
            <div class="loading-spinner"></div>
            <span class="loading-text">加载中</span>
        </div>

        <div v-else-if="error" class="error card">
            <p class="text-error">加载题目失败: {{ error }}</p>
            <button class="button button-primary" @click="fetchProblemDetail">重试</button>
        </div>

        <div v-else-if="problem" class="grid grid-cols-2">
            <!-- 左侧面板：题目描述、日志和波形 -->
            <div class="flex flex-col gap-lg">
                <!-- 描述部分 -->
                <CollapsibleSection title="题目描述" v-model:isExpanded="descriptionExpanded">
                    <div class="card-body">
                        <h1 class="title">{{ problem.title }}</h1>
                        <div class="difficulty text-lg mb-sm"
                            :class="{
                                'text-success': problem.difficulty === '简单',
                                'text-warning': problem.difficulty === '中等',
                                'text-error': problem.difficulty === '困难'
                            }">
                            <b>难度: {{ problem.difficulty }}</b>
                        </div>

                        <div v-if="problem.tags && problem.tags.length" class="flex flex-wrap gap-xs mb-md">
                            <span v-for="(tag, index) in problem.tags" :key="index" class="tag">
                                {{ tag }}
                            </span>
                        </div>

                        <MarkdownRenderer :content="problem.description" class="text-base" />
                    </div>
                </CollapsibleSection>

                <!-- 日志部分 -->
                <CollapsibleSection title="运行日志" v-model:isExpanded="logExpanded" :status="logSectionStatus">
                    <div class="card-body">
                        <div class="log-header">
                            <div class="status-info">
                                <span class="status-badge" :class="logSectionStatus" v-if="currentSubmissionId && currentLog">
                                    {{ logSectionStatus === 'success' ? '测试通过' : logSectionStatus === 'error' ? '测试失败' : '等待测试' }}
                                </span>
                                <button @click="getAiAnalysis" 
                                    class="button button-sm status-badge button-info" 
                                    :class="{ 'is-analyzing': isAnalyzing }"
                                    :disabled="isAnalyzing">
                                    {{ isAnalyzing ? '分析中' : 'AI分析' }}
                                </button>
                            </div>
                        </div>
                        
                        <LogViewer :content="currentLog" class="mb-md" />
                        
                        <!-- AI分析结果显示 -->
                        <transition 
                            name="slide-fade"
                            @enter="el => el.style.height = el.scrollHeight + 'px'"
                            @leave="el => el.style.height = '0'">
                            <div v-if="showAiAnalysis && aiAnalysisResult" 
                                class="ai-analysis-container mt-lg pt-md border-t"
                                :class="{ 'is-entering': isAnalysisEntering }">
                                <div class="card card-info">
                                    <MarkdownRenderer :content="aiAnalysisResult" class="text-base" />
                                </div>
                            </div>
                        </transition>
                    </div>
                </CollapsibleSection>

                <!-- 波形部分 -->
                <CollapsibleSection title="波形显示" v-model:isExpanded="waveformExpanded">
                    <div class="card-body">
                        <WaveformViewer :vcdContent="currentWaveform" />
                    </div>
                </CollapsibleSection>
            </div>

            <!-- 右侧面板：代码编辑器 -->
            <div class="flex flex-col gap-md">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">代码编辑器</h2>
                        <div class="button-group">
                            <button class="button button-secondary" @click="loadDraft">加载草稿</button>
                            <button class="button button-secondary" @click="saveDraft">保存草稿</button>
                            <button class="button button-danger" @click="clearEditor">清空</button>
                        </div>
                    </div>

                    <div class="card-body p-0">
                        <VerilogEditor ref="editorRef" v-model="verilogCode" class="editor-container" />
                    </div>

                    <div class="card-footer">
                        <div class="flex justify-between items-center">
                            <span class="text-secondary text-sm italic">代码会每分钟自动保存</span>
                            <button class="button button-primary" @click="submitSolution">提交解答</button>
                        </div>
                    </div>
                </div>
                <SubmitHistory ref="historyRef" :problem-id="problemId" @select-submission="handleHistorySelect" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.problem-submit {
    padding: var(--spacing-lg);
}

.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-md);
    padding: var(--spacing-xl);
}

.editor-container {
    height: calc(100vh - 300px);
    min-height: 400px;
    border-radius: 0;
    border: none;
}

.tag {
    display: inline-block;
    padding: var(--spacing-xs) var(--spacing-sm);
    background-color: var(--surface-color);
    color: var(--text-secondary);
    border-radius: var(--radius-sm);
    font-size: 0.875rem;
    border: 1px solid var(--border-color);
}

.sticky {
    position: sticky;
    top: var(--spacing-lg);
    height: calc(100vh - var(--spacing-lg) * 2);
}

/* 响应式调整 */
@media (max-width: 1200px) {
    .grid-cols-2 {
        grid-template-columns: 1fr;
    }

    .sticky {
        position: static;
        height: auto;
    }

    .editor-container {
        height: 500px;
    }
}

@media (max-width: 768px) {
    .problem-submit {
        padding: var(--spacing-md);
    }

    .card-header {
        flex-direction: column;
        gap: var(--spacing-sm);
    }

    .button-group {
        width: 100%;
        display: flex;
        gap: var(--spacing-xs);
    }

    .button-group .button {
        flex: 1;
    }
}

/* AI分析按钮样式 */
.ai-analyze-btn {
    position: relative;
    margin: 0;
}

.ai-analyze-btn.is-analyzing {
    padding-right: 36px;
}

/* AI分析结果容器动画 */
.ai-analysis-container {
    overflow: hidden;
    transition: all var(--transition-normal);
    opacity: 1;
    transform: translateY(0);
}

.ai-analysis-container.is-entering {
    opacity: 0;
    transform: translateY(20px);
}

.slide-fade-enter-active,
.slide-fade-leave-active {
    transition: all var(--transition-normal);
    max-height: 2000px; /* 设置一个合适的最大高度 */
}

.slide-fade-enter-from,
.slide-fade-leave-to {
    opacity: 0;
    transform: translateY(20px);
    max-height: 0;
}

/* 确保卡片内容有合适的间距 */
.card-info {
    padding: var(--spacing-md);
    margin-top: var(--spacing-md);
    background-color: color-mix(in srgb, var(--info-color) 5%, var(--background-color));
    border: 1px solid color-mix(in srgb, var(--info-color) 30%, var(--border-color));
}

.log-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-md);
    padding-bottom: var(--spacing-sm);
    border-bottom: 1px solid var(--border-color);
}

.status-info {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
}

.status-badge {
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--radius-sm);
    font-size: 0.875rem;
    font-weight: 500;
}

.status-badge.success {
    background-color: color-mix(in srgb, var(--success-color) 10%, transparent);
    color: var(--success-color);
    border: 1px solid var(--success-color);
}

.status-badge.error {
    background-color: color-mix(in srgb, var(--error-color) 10%, transparent);
    color: var(--error-color);
    border: 1px solid var(--error-color);
}

.status-badge.button-info {
    position: relative;
    color: var(--info-color);
    background-color: color-mix(in srgb, var(--info-color) 10%, transparent);
    border: 1px solid var(--info-color);
    transition: all var(--transition-fast);
}

.status-badge.button-info:hover {
    background-color: color-mix(in srgb, var(--info-color) 15%, transparent);
}

.status-badge.button-info.is-analyzing {
    border-color: transparent;
}

.status-badge.button-info.is-analyzing::before {
    content: '';
    position: absolute;
    inset: -1px;
    border-radius: inherit;
    padding: 1px;
    background: linear-gradient(
        90deg,
        var(--info-color) 0%,
        transparent 50%,
        var(--info-color) 100%
    );
    background-size: 200% 100%;
    mask: 
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);
    mask-composite: exclude;
    -webkit-mask: 
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);
    -webkit-mask-composite: destination-out;
    animation: flow-border 2s linear infinite;
}

@keyframes flow-border {
    from {
        background-position: 100% 0;
    }
    to {
        background-position: -100% 0;
    }
}

</style>