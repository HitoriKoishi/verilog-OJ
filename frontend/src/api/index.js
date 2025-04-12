import axios from 'axios';

// 创建axios实例
const api = axios.create({
    baseURL: 'http://localhost:5000/api', // Flask后端地址
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 题目相关接口
export const problemApi = {
    // 获取题目列表
    getProblems() {
        return api.get('/problems');
    },

    // 获取题目详情
    getProblemById(id) {
        return api.get(`/problems/${id}`);
    },

    // 提交代码
    submitCode(problemId, code) {
        return api.post(`/problems/${problemId}/submit`, { code });
    },

    // 获取提交状态
    getSubmissionStatus(submissionId) {
        return api.get(`/submissions/${submissionId}`);
    }
};

// 用户相关接口
export const userApi = {
    // 登录
    login(username, password) {
        return api.post('/auth/login', { username, password });
    },

    // 注册
    register(username, password, email) {
        return api.post('/auth/register', { username, password, email });
    }
};

export default api;