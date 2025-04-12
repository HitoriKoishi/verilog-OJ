import axios from 'axios';

// 设置基础URL
const apiClient = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json'
    }
});

export default {
    // 获取所有题目
    getProblems() {
        return apiClient.get('/problems');
    },

    // 获取单个题目详情
    getProblem(id) {
        return apiClient.get(`/problems/${id}`);
    },

    // 提交解答
    submitSolution(problemId, code) {
        return apiClient.post('/submissions', { problemId, code });
    }
};
