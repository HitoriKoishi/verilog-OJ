<script setup>
import { ref, onMounted, onUnmounted, shallowRef, nextTick } from 'vue';
import message from '../utils/message'  // 导入消息工具
import { useRoute } from 'vue-router';
import axios from 'axios';
import { marked } from 'marked'; // 重新引入 marked 用于渲染 Markdown
import { EditorState } from '@codemirror/state';
import { EditorView } from '@codemirror/view';
// 从 codemirror 主包中导入，而不是从 basic-setup
import { basicSetup } from 'codemirror';
import { javascript } from '@codemirror/lang-javascript';
import { problemApi } from '../api';
import { submissionApi } from '../api';
const route = useRoute();
const problemId = route.params.id;

const problem = ref(null);
const loading = ref(true);
const error = ref(null);
const verilogCode = ref('');
const editorElement = ref(null);
const editorView = shallowRef(null);
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

        // 渲染 Markdown 内容
        if (problem.value.description) {
            // 设置 marked 选项，提高安全性
            const renderer = new marked.Renderer();
            marked.setOptions({
                renderer: renderer,
                gfm: true,
                breaks: true,
                sanitize: false,
                smartLists: true,
                smartypants: false,
                xhtml: false
            });

            // 移除第一个一级标题，只需提取文档内容中第一个一级标题后的所有内容
            const lines = problem.value.description.split('\n');
            let firstH1Index = -1;
            
            // 寻找第一个一级标题的位置
            for (let i = 0; i < lines.length; i++) {
                if (lines[i].startsWith('# ')) {
                    firstH1Index = i;
                    break;
                }
            }
            
            // 如果找到了一级标题，则跳过它
            if (firstH1Index !== -1) {
                const contentWithoutFirstH1 = lines.slice(firstH1Index + 1).join('\n');
                problem.value.htmlContent = marked(contentWithoutFirstH1);
            } else {
                problem.value.htmlContent = marked(problem.value.description);
            }
        } else {
            problem.value.htmlContent = '<p>没有题目描述内容</p>';
        }

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

// 提交解答
const submitSolution = async () => {
    if (!verilogCode.value.trim()) {
        message.warning('请输入Verilog代码');
        return;
    }

    try {
        const submitResponse = await problemApi.submitSolution(problemId, verilogCode.value);

        if (!submitResponse.data || !submitResponse.data.submission_id) {
            throw new Error('提交失败: 服务器返回无效的提交ID');
        }

        currentSubmissionId.value = submitResponse.data.submission_id;
        message.success('代码提交成功，正在评测...');
        
        // 自动关闭描述，打开日志
        descriptionExpanded.value = false;
        logExpanded.value = true;
        
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

        if (submissionData.status === 'success') {
            message.success('提交成功！您的代码已通过测试');
        } else {
            message.error(`提交失败: ${submissionData.error_code}`);
        }
    } catch (err) {
        console.error('获取提交结果失败:', err);
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

const initCodeMirrorEditor = async () => {
    console.log('初始化编辑器开始', editorElement.value);
    if (!editorElement.value) {
        console.error('编辑器容器元素不存在');
        return;
    }

    try {
        // 确保之前的编辑器实例被销毁
        if (editorView.value) {
            editorView.value.destroy();
        }

        // 清空容器内容，确保没有残留元素
        editorElement.value.innerHTML = '';

        const startState = EditorState.create({
            doc: verilogCode.value || '// 在此处编写Verilog代码',
            extensions: [
                basicSetup,
                javascript(), // 作为临时的语法高亮，未来可替换为Verilog语法高亮
                EditorView.updateListener.of(update => {
                    if (update.docChanged) {
                        verilogCode.value = update.state.doc.toString();
                    }
                })
            ]
        });

        // 创建新的编辑器实例
        editorView.value = new EditorView({
            state: startState,
            parent: editorElement.value
        });

        console.log('编辑器初始化成功');
    } catch (err) {
        console.error('初始化编辑器失败:', err);
        // 出现错误时添加错误提示
        editorElement.value.innerHTML = `<div style="color:red; padding:10px;">
            编辑器加载失败: ${err.message}
            <br>
            <button onclick="location.reload()">刷新页面重试</button>
        </div>`;
    }
};

// 更新编辑器内容
const updateEditorContent = (content) => {
    if (!editorView.value) return;
    const transaction = editorView.value.state.update({
        changes: {
            from: 0,
            to: editorView.value.state.doc.length,
            insert: content
        }
    });
    editorView.value.dispatch(transaction);
};

// 清空编辑器内容
const clearEditor = () => {
    verilogCode.value = '';
    if (editorView.value) {
        updateEditorContent('');
    }
};

// 改进 onMounted 逻辑，在DOM渲染完成后再初始化编辑器
onMounted(async () => {
    console.log('组件挂载');
    await fetchProblemDetail();
    await loadDraft();

    // 使用 nextTick 确保 DOM 已更新，并添加延迟确保渲染完成
    nextTick(() => {
        // 添加一点延迟以确保DOM完全渲染
        setTimeout(() => {
            console.log('DOM 更新后初始化编辑器');
            initCodeMirrorEditor();
        }, 300);
    });
});

let autoSaveInterval;
onMounted(() => {
    autoSaveInterval = setInterval(saveDraft, 60000);
});

onUnmounted(() => {
    clearInterval(autoSaveInterval);
    if (editorView.value) {
        editorView.value.destroy();
    }
});

// 当verilogCode从外部被更新时更新编辑器
const updateCodeMirror = (code) => {
    verilogCode.value = code;
    if (editorView.value) {
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
                <div class="section description-section">
                    <div class="section-header" @click="descriptionExpanded = !descriptionExpanded">
                        <h2>题目描述</h2>
                        <span class="expand-icon">{{ descriptionExpanded ? '▼' : '▶' }}</span>
                    </div>
                    <div v-show="descriptionExpanded" class="section-content problem-description">
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

                        <!-- 使用 Markdown 渲染的内容 -->
                        <div class="markdown-content" v-html="problem.htmlContent"></div>
                    </div>
                </div>

                <!-- 日志部分 -->
                <div class="section log-section">
                    <div class="section-header" @click="logExpanded = !logExpanded">
                        <h2>运行日志</h2>
                        <span class="expand-icon">{{ logExpanded ? '▼' : '▶' }}</span>
                    </div>
                    <div v-show="logExpanded" class="section-content log-content">
                        <pre v-if="currentLog">{{ currentLog }}</pre>
                        <p v-else>暂无日志</p>
                    </div>
                </div>

                <!-- 波形部分 -->
                <div class="section waveform-section">
                    <div class="section-header" @click="waveformExpanded = !waveformExpanded">
                        <h2>波形显示</h2>
                        <span class="expand-icon">{{ waveformExpanded ? '▼' : '▶' }}</span>
                    </div>
                    <div v-show="waveformExpanded" class="section-content waveform-content">
                        <pre v-if="currentWaveform">{{ currentWaveform }}</pre>
                        <p v-else>暂无波形数据</p>
                    </div>
                </div>
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

                    <!-- 明确设置ref并添加id以便于调试 -->
                    <div ref="editorElement" id="codemirror-editor" class="codemirror-container"></div>

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
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); /* 修改为两列布局 */
    gap: 20px;
}

/* 左侧容器 */
.left-panel {
    display: flex;
    flex-direction: column;
    gap: 20px;
    max-height: calc(100vh - 100px); /* 设置最大高度，留出顶部和底部空间 */
    overflow-y: auto; /* 允许滚动 */
}

/* 右侧容器 */
.right-panel {
    position: sticky; /* 使编辑器固定 */
    top: 20px; /* 距离顶部距离 */
    height: calc(100vh - 100px); /* 设置高度 */
    display: flex;
    flex-direction: column;
}

.problem-description {
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 8px;
    max-height: 800px;
    overflow-y: auto;
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

/* 修改描述内容样式为 markdown-content */
.markdown-content {
    border-top: 1px solid #ddd;
    padding-top: 15px;
    margin-top: 15px;
}

/* 添加图片样式控制 */
.markdown-content :deep(img) {
    max-width: 90%;  /* 图片最大宽度为容器的90% */
    height: auto;    /* 保持图片比例 */
    display: block;  /* 块级显示使居中生效 */
    margin: 15px auto; /* 上下15px边距，左右自动居中 */
    border-radius: 4px; /* 圆角边框 */
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) {
    margin-top: 1em;
    margin-bottom: 0.5em;
}

.markdown-content :deep(p) {
    text-indent: 2em;
    margin: 0.5em 0;
}

/* 列表样式 */
.markdown-content :deep(ul),
.markdown-content :deep(ol) {
    padding-left: 2em;
    margin: 0.5em 0;
}

.markdown-content :deep(li) {
    margin: 0.3em 0;
}

/* 嵌套列表的缩进 */
.markdown-content :deep(ul ul),
.markdown-content :deep(ul ol),
.markdown-content :deep(ol ul),
.markdown-content :deep(ol ol) {
    margin: 0.2em 0;
}

.markdown-content :deep(pre) {
    background-color: #f5f5f5;
    padding: 12px;
    border-radius: 4px;
    overflow-x: auto;
}

.markdown-content :deep(code) {
    font-family: 'Consolas', 'Monaco', monospace;
    background-color: #f0f0f0;
    padding: 2px 4px;
    border-radius: 3px;
    font-size: 0.9em;
}

.markdown-content :deep(table) {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

.markdown-content :deep(th),
.markdown-content :deep(td) {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

.markdown-content :deep(th) {
    background-color: #f2f2f2;
}

.description-content {
    display: none;
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

.codemirror-container {
    flex: 1;
    min-height: 0; /* 防止溢出 */
    width: 100%;
    border: 1px solid #ddd;
    border-radius: 4px;
    overflow: hidden;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 14px;
    background-color: #f5f5f5;
    /* 添加背景色以便于观察容器是否正确渲染 */
}

.codemirror-container :deep(.cm-editor) {
    height: 100%;
    width: 100%;
}

.codemirror-container :deep(.cm-scroller) {
    overflow: auto;
    font-family: 'Consolas', 'Monaco', monospace;
}

.codemirror-container :deep(.cm-content) {
    font-family: 'Consolas', 'Monaco', monospace;
    padding: 4px;
}

.codemirror-container :deep(.cm-line) {
    padding: 0 4px;
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

    .codemirror-container {
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

.section {
    margin-bottom: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
}

.section-header {
    padding: 12px 20px;
    background-color: #f8f9fa;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    user-select: none;
}

.section-header:hover {
    background-color: #e9ecef;
}

.expand-icon {
    font-size: 18px;
    color: #666;
}

.section-content {
    padding: 20px;
    background-color: white;
}

.log-content,
.waveform-content {
    max-height: 400px;
    overflow-y: auto;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 14px;
    background-color: #f5f5f5;
    padding: 12px;
    border-radius: 4px;
}

pre {
    margin: 0;
    white-space: pre-wrap;
    word-wrap: break-word;
}

/* 调整布局 */
.problem-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.description-section,
.log-section,
.waveform-section {
    width: 100%;
}

/* 响应式布局 */
@media (max-width: 900px) {
    .section-content {
        padding: 15px;
    }
}
</style>