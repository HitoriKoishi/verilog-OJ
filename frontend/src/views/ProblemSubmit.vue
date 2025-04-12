<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { marked } from 'marked'; // 重新引入 marked 用于渲染 Markdown

const route = useRoute();
const problemId = route.params.id;

const problem = ref(null);
const loading = ref(true);
const error = ref(null);
const verilogCode = ref('');

// 获取单个题目的详细信息
const fetchProblemDetail = async () => {
    loading.value = true;
    error.value = null;

    try {
        // 修改请求路径，直接使用后端API路径
        const response = await axios.get(`http://localhost:5000/problems/${problemId}`, {
            timeout: 10000,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            withCredentials: true // 确保发送 cookies
        });

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

            problem.value.htmlContent = marked(problem.value.description);
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
        alert('请输入Verilog代码');
        return;
    }

    try {
        const submitResponse = await axios.post(`/api/problems/${problemId}/submit`, {
            code: verilogCode.value
        }, {
            timeout: 10000,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });

        if (!submitResponse.data || !submitResponse.data.submission_id) {
            throw new Error('提交失败: 服务器返回无效的提交ID');
        }

        const submissionId = submitResponse.data.submission_id;
        console.log('提交成功，获取提交ID:', submissionId);

        setTimeout(() => {
            checkSubmissionResult(submissionId);
        }, 1000);

    } catch (err) {
        console.error('提交解答失败:', err);
        alert('提交失败: ' + (err.response?.data?.error || err.message || '未知错误'));
    }
};

// 轮询检查提交结果
const checkSubmissionResult = async (submissionId) => {
    try {
        const resultResponse = await axios.get(`/api/submissions/${submissionId}`, {
            headers: {
                'Accept': 'application/json'
            }
        });

        const submissionData = resultResponse.data;

        if (submissionData.status === 'queued' || submissionData.status === 'running') {
            console.log(`提交状态: ${submissionData.status}，继续等待...`);
            setTimeout(() => {
                checkSubmissionResult(submissionId);
            }, 3000);
            return;
        }

        if (submissionData.status === 'success') {
            alert('提交成功！您的代码已通过测试');
        } else {
            let errorMessage = '提交失败';
            if (submissionData.error_code) {
                errorMessage += `: ${submissionData.error_code}`;
            }
            alert(errorMessage);
        }

        if (submissionData.log_path) {
            console.log('日志文件路径:', submissionData.log_path);
        }

        if (submissionData.waveform_path) {
            console.log('波形文件路径:', submissionData.waveform_path);
        }

    } catch (err) {
        console.error('获取提交结果失败:', err);
        alert('获取提交结果失败: ' + (err.response?.data?.error || err.message || '未知错误'));
    }
};

// 保存代码草稿
const saveDraft = async () => {
    if (!verilogCode.value.trim()) {
        return;
    }

    try {
        await axios.post(`/api/problems/${problemId}/save`, {
            code: verilogCode.value
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        console.log('代码草稿已保存');
    } catch (err) {
        console.error('保存代码草稿失败:', err);
    }
};

// 加载代码草稿
const loadDraft = async () => {
    try {
        const response = await axios.get(`/api/problems/${problemId}/load`, {
            headers: {
                'Accept': 'application/json'
            }
        });

        if (response.data.status === 'success' && response.data.draft_code) {
            verilogCode.value = response.data.draft_code;
            console.log('已加载之前保存的代码草稿, 保存时间:', response.data.draft_time);
        }
    } catch (err) {
        console.error('加载代码草稿失败:', err);
    }
};

onMounted(() => {
    fetchProblemDetail();
    loadDraft();
});

let autoSaveInterval;
onMounted(() => {
    autoSaveInterval = setInterval(saveDraft, 60000);
});

onUnmounted(() => {
    clearInterval(autoSaveInterval);
});
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

                <!-- 使用 Markdown 渲染的内容 -->
                <div class="markdown-content" v-html="problem.htmlContent"></div>
            </div>

            <div class="code-editor">
                <h2>代码编辑器</h2>
                <div class="editor-controls">
                    <button @click="loadDraft" class="control-btn">加载草稿</button>
                    <button @click="saveDraft" class="control-btn">保存草稿</button>
                    <button @click="verilogCode = ''" class="control-btn clear-btn">清空</button>
                </div>
                <textarea v-model="verilogCode" placeholder="请在此输入您的Verilog代码..." rows="15"></textarea>

                <div class="submit-section">
                    <span class="auto-save-info">代码会每分钟自动保存</span>
                    <button @click="submitSolution" class="submit-btn">提交解答</button>
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
    display: flex;
    flex-direction: column;
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

textarea {
    width: 100%;
    padding: 12px;
    font-family: 'Consolas', 'Monaco', monospace;
    border: 1px solid #ddd;
    border-radius: 4px;
    resize: vertical;
    font-size: 14px;
    line-height: 1.5;
    height: 500px;
    tab-size: 4;
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

@media (max-width: 900px) {
    .problem-container {
        grid-template-columns: 1fr;
    }

    .problem-description,
    .code-editor {
        max-height: none;
    }
}
</style>