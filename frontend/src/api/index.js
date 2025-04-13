import axios from 'axios';

// 创建axios实例
const apiClient = axios.create({
    baseURL: '/api',  // 使用Vite代理前缀
    headers: {
        'Content-Type': 'application/json'
    },
    withCredentials: true  // 允许跨域请求携带凭证（cookie）
});

export const problemApi = {
    // 获取题目列表
    getProblems() {
        return apiClient.get('/problem');
    },

    // 获取题目详情
    getProblem(id) {
        return apiClient.get(`/problem/${id}`);
    },

    // 保存代码草稿
    saveDraft(id, code) {
        return apiClient.post(`/problem/${id}/save`, { code });
    },

    // 加载代码草稿
    loadDraft(id) {
        return apiClient.get(`/problem/${id}/load`);
    },

    // 提交代码
    submitSolution(id, code) {
        return apiClient.post(`/problem/${id}/submit`, { code });
    }
};

export const userApi = {
    // 登录
    login(username, password) {
        return apiClient.post('/user/login', { username, password });
    },

    // 注册
    register(username, password, email) {
        return apiClient.post('/user/register', { username, password, email });
    },

    // 注销
    logout() {
        return apiClient.post('/user/logout');
    },

    // 检查登录状态
    checkAuth() {
        return apiClient.get('/user/check_auth');
    },

    // 获取用户提交历史
    getSubmissions(userId) {
        return apiClient.get(`/user/${userId}/submission`);
    }
};

export const submissionApi = {
    // 获取提交状态
    getSubmission(submissionId) {
        return apiClient.get(`/submission/${submissionId}`);
    }
};

export default {
    problem: problemApi,
    user: userApi,
    submission: submissionApi
};