import axios from 'axios';

// 创建axios实例
<<<<<<< Updated upstream
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
<<<<<<< HEAD
        return apiClient.post('/login', { username, password });
=======
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
>>>>>>> Stashed changes
=======
        return apiClient.post('/user/login', { username, password });
>>>>>>> main
    },

    // 注册
    register(username, password, email) {
<<<<<<< HEAD
<<<<<<< Updated upstream
        return apiClient.post('/register', { username, password, email });
=======
        return apiClient.post('/user/register', { username, password, email });
>>>>>>> main
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
=======
        return api.post('/auth/register', { username, password, email });
    }
};

export default api;
>>>>>>> Stashed changes
