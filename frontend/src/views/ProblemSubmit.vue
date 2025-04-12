<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { marked } from 'marked'; // 安装 marked 用于渲染 Markdown

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
        const response = await axios.get(`/api/problems/${problemId}`);
        problem.value = response.data;
        // 将markdown文档内容存储到problem对象中
        if (response.data.content) {
            problem.value.htmlContent = marked(response.data.content);
        }
    } catch (err) {
        console.error('获取题目详情失败:', err);
        error.value = err.message || '获取题目详情失败';
    } finally {
        loading.value = false;
    }
};

const submitSolution = async () => {
    if (!verilogCode.value.trim()) {
        alert('请输入Verilog代码');
        return;
    }

    try {
        const response = await axios.post(`/api/submissions`, {
            problemId: problemId,
            code: verilogCode.value
        });

        alert(response.data.success ? '提交成功！' : '提交失败');
        // 可以添加导航到结果页面的逻辑
    } catch (err) {
        console.error('提交解答失败:', err);
        alert('提交失败: ' + (err.message || '未知错误'));
    }
};

onMounted(() => {
    fetchProblemDetail();
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

                <!-- 渲染Markdown内容 -->
                <div class="markdown-content" v-html="problem.htmlContent"></div>
            </div>

            <div class="code-editor">
                <h2>代码编辑器</h2>
                <textarea v-model="verilogCode" placeholder="请在此输入您的Verilog代码..." rows="15"></textarea>

                <div class="submit-section">
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
}

.difficulty {
    font-weight: bold;
    margin-bottom: 15px;
}

.markdown-content {
    border-top: 1px solid #ddd;
    padding-top: 15px;
}

.code-editor {
    display: flex;
    flex-direction: column;
}

textarea {
    width: 100%;
    padding: 12px;
    font-family: monospace;
    border: 1px solid #ddd;
    border-radius: 4px;
    resize: vertical;
    font-size: 14px;
    line-height: 1.5;
}

.submit-section {
    margin-top: 15px;
    display: flex;
    justify-content: flex-end;
}

.submit-btn {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
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
</style>