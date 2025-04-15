<script setup>
// 移除原有的编辑器相关导入
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

        // 使用后端返回的数据结构
        problem.value = {
            id: response.data.id,
            title: response.data.title,
            description: response.data.document,
            difficulty: response.data.difficulty,
            tags: response.data.tags,
            codeTemplate: response.data.code_template
        };

        // 如果有代码模板，设置到编辑器中
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
    // 先关闭描述部分
    descriptionExpanded.value = false;
    
    // 等待一小段时间后打开日志部分，确保动画能够顺序执行
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // 打开日志部分
    logExpanded.value = true;
};

// 提交解答
const submitSolution = async () => {
    if (!verilogCode.value.trim()) {
        message.warning('请输入Verilog代码');
        return;
    }

    // 重置状态
    logSectionStatus.value = 'default';

    try {
        // 清空AI分析结果
        aiAnalysisResult.value = '';
        showAiAnalysis.value = false;
        
        const submitResponse = await problemApi.submitSolution(problemId, verilogCode.value);

        if (!submitResponse.data || !submitResponse.data.submission_id) {
            throw new Error('提交失败: 服务器返回无效的提交ID');
        }

        currentSubmissionId.value = submitResponse.data.submission_id;
        message.success('代码提交成功，正在评测...');
        
        // 使用新的动画控制函数
        await toggleSections();
        
        setTimeout(() => {
            checkSubmissionResult(currentSubmissionId.value);
        }, 1000);

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

        // 获取日志和波形
        await fetchLogAndWaveform(submissionId);

        // 更新日志状态
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

// 改进 onMounted 逻辑，在DOM渲染完成后再初始化编辑器
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

// 当verilogCode从外部被更新时更新编辑器
const updateCodeMirror = (code) => {
    verilogCode.value = code;
    if (editorRef.value) {
        updateEditorContent(code);
    }
};

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

// 添加AI分析相关的状态
const isAnalyzing = ref(false);
const aiAnalysisResult = ref('');
const showAiAnalysis = ref(false);

// 获取AI分析
const getAiAnalysis = async () => {
    if (!currentSubmissionId.value) {
        message.warning('请先提交代码');
        return;
    }
    
    try {
        isAnalyzing.value = true;
        message.info('正在请求AI分析，请稍候...');
        
        const response = await aiApi.getAnalysis(currentSubmissionId.value);
        
        if (response.data && response.data.analysis) {
            aiAnalysisResult.value = response.data.analysis;
            showAiAnalysis.value = true;
            message.success('AI分析完成');
        } else {
            throw new Error('分析结果为空');
        }
    } catch (err) {
        console.error('获取AI分析失败:', err);
        message.error('获取AI分析失败: ' + (err.response?.data?.error || err.message || '未知错误'));
        aiAnalysisResult.value = '获取分析失败: ' + (err.response?.data?.error || err.message || '未知错误');
    } finally {
        isAnalyzing.value = false;
    }
};
</script>

<template>
  <div class="problem-submit">
    <div v-if="loading" class="loading">
      加载中...
    </div>

    <div v-else-if="error" class="error">
      <p>加载题目失败: {{ error }}</p>
      <button @click="fetchProblemDetail">重试</button>
    </div>

    <div v-else-if="problem" class="problem-container">
      <!-- 左侧面板：题目描述、日志和波形 -->
      <div class="left-panel">
        <!-- 描述部分 -->
        <CollapsibleSection 
          title="题目描述" 
          v-model:isExpanded="descriptionExpanded"
        >
          <div class="problem-description">
            <h1>{{ problem.title }}</h1>
            <div class="difficulty"
              :style="{ color: problem.difficulty === '简单' ? 'green' : (problem.difficulty === '中等' ? 'orange' : 'red') }">
              难度: {{ problem.difficulty }}
            </div>

            <div class="tags-container" v-if="problem.tags && problem.tags.length">
              <span v-for="(tag, index) in problem.tags" :key="index" class="tag">
                {{ tag }}
              </span>
            </div>

            <MarkdownRenderer :content="problem.description" />
          </div>
        </CollapsibleSection>

        <!-- 日志部分 -->
        <CollapsibleSection 
          title="运行日志" 
          v-model:isExpanded="logExpanded"
          :status="logSectionStatus"
        >
          <div>
            <div v-if="currentSubmissionId && currentLog" class="log-actions">
              <button 
                @click="getAiAnalysis" 
                class="ai-analyze-btn"
                :disabled="isAnalyzing"
              >
                {{ isAnalyzing ? '分析中...' : 'AI智能分析' }}
              </button>
            </div>
            <LogViewer :content="currentLog" />
            <!-- AI分析结果显示 -->
            <div v-if="showAiAnalysis && aiAnalysisResult" class="ai-analysis-section">
              <h3>AI分析结果</h3>
              <div class="ai-analysis-content" v-html="marked(aiAnalysisResult)"></div>
            </div>
          </div>
        </CollapsibleSection>

        <!-- 波形部分 -->
        <CollapsibleSection 
          title="波形显示" 
          v-model:isExpanded="waveformExpanded"
        >
          <WaveformViewer :vcdContent="currentWaveform" />
        </CollapsibleSection>
      </div>

      <!-- 右侧面板：代码编辑器 -->
      <div class="right-panel">
        <div class="code-editor">
          <h2>代码编辑器</h2>
          <div class="editor-controls">
            <button @click="loadDraft" class="control-btn">加载草稿</button>
            <button @click="saveDraft" class="control-btn">保存草稿</button>
            <button @click="clearEditor" class="control-btn clear-btn">清空</button>
          </div>

          <VerilogEditor
            ref="editorRef"
            v-model="verilogCode"
            class="editor-container"
          />

          <div class="submit-section">
            <span class="auto-save-info">代码会每分钟自动保存</span>
            <button @click="submitSolution" class="submit-btn">提交解答</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.problem-submit {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.problem-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    min-height: calc(100vh - 100px);
    width: 100%;
}

.left-panel {
    display: flex;
    flex-direction: column;
    gap: 20px;
    /* 修改最大高度设置，让其根据内容自动调整 */
    /* max-height: calc(100vh - 100px); */
    /* overflow-y: auto; */
}

.right-panel {
    display: flex;
    flex-direction: column;
    position: sticky;
    top: 20px;
    height: calc(100vh - 100px);
    min-width: 0;
}

.difficulty {
    font-weight: bold;
    margin-bottom: 15px;
}

.tags-container {
    margin: 10px 0;
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
}

.tag {
    background-color: #e0f2f1;
    color: #00796b;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8em;
    display: inline-block;
}

.code-editor {
    flex: 1;
    display: flex;
    flex-direction: column;
    height: 100%;
}

.editor-controls {
    display: flex;
    margin-bottom: 10px;
    gap: 10px;
}

.control-btn {
    padding: 6px 12px;
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.2s;
}

.control-btn:hover {
    background-color: #e0e0e0;
}

.clear-btn {
    background-color: #ffeeee;
}

.clear-btn:hover {
    background-color: #ffdddd;
}

.editor-container {
  flex: 1;
  min-height: 0;
}

.submit-section {
    margin-top: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.auto-save-info {
    color: #666;
    font-size: 0.9em;
    font-style: italic;
}

.submit-btn {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.2s;
}

.submit-btn:hover {
    background-color: #45a049;
}

.loading,
.error {
    padding: 20px;
    text-align: center;
}

.error {
    color: red;
}

@media (max-width: 1200px) {
    .problem-container {
        grid-template-columns: 1fr; /* 在小屏幕上变为单列 */
    }

    .right-panel {
        position: static;
        height: auto;
    }

    .editor-container {
        height: 500px; /* 在小屏幕上固定高度 */
    }
}

@media (max-width: 900px) {
    .problem-container {
        grid-template-columns: 1fr;
    }

    .problem-description,
    .code-editor {
        max-height: none;
    }
}

pre {
    margin: 0;
    white-space: pre-wrap;
    word-wrap: break-word;
}

/* 响应式布局 */
@media (max-width: 900px) {
    .section-content {
        padding: 15px;
    }
}

.problem-description,
.waveform-content {
    background-color: #ffffff;
    border-radius: 4px;
    padding: 20px;
    margin: 0;
    /* border: 1px solid #f0f0f0; */
    /* box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05); */
}

/* 日志和波形特有的样式 */
.waveform-content {
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 14px;
    max-height: 400px;
    overflow-y: auto;
}

/* 暗色主题支持 */
@media (prefers-color-scheme: dark) {
    .problem-description,
    .waveform-content {
        background-color: #1a1a1a;
        border-color: #2d2d2d;
        color: #e0e0e0;
    }
}

/* 添加AI分析相关样式 */
.log-actions {
    margin-bottom: 10px;
    display: flex;
    justify-content: flex-end;
}

.ai-analyze-btn {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.2s;
}

.ai-analyze-btn:hover {
    background-color: #0056b3;
}

.ai-analyze-btn:disabled {
    background-color: #6c757d;
    cursor: not-allowed;
}

.ai-analysis-section {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px dashed #ccc;
}

.ai-analysis-section h3 {
    color: #007bff;
    margin-bottom: 10px;
}

.ai-analysis-content {
    background-color: #f0f7ff;
    padding: 15px;
    border-radius: 4px;
    white-space: normal;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.5;
}

.ai-analysis-content :deep(pre) {
    background-color: #f5f5f5;
    padding: 10px;
    border-radius: 4px;
    overflow-x: auto;
}

.ai-analysis-content :deep(code) {
    font-family: 'Consolas', 'Monaco', monospace;
    background-color: #f0f0f0;
    padding: 2px 4px;
    border-radius: 3px;
    font-size: 0.9em;
}
</style>