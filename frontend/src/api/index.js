import axios from 'axios';

// 创建axios实例
const apiClient = axios.create({
    baseURL: '/api',  // 使用Vite代理前缀
    headers: {
        'Content-Type': 'application/json'
    },
    withCredentials: true  // 允许跨域请求携带凭证
});

export const problemApi = {
    // 获取题目列表
    getProblems() {
        return apiClient.get('/problem/all');
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
    },

    // 获取题目状态
    getProblemStatus() {
        return apiClient.get('/problem/status');
    },

    // 获取用户单一问题提交历史
    getProblemSubmitHistory(id) {
        return apiClient.get(`/problem/${id}/submit_history`);
    },
};

export const userApi = {
    // 登录
    login(username, password) {
        return apiClient.post('/user/login', {
            username: username,
            password: password
        });
    },

    // 注册
    register(username, password, email) {
        return apiClient.post('/user/register', {
            username: username,
            password: password,
            email: email
        });
    },

    // 注销
    logout() {
        return apiClient.post('/user/logout');
    },

    // 检查登录状态
    checkAuth() {
        return apiClient.get('/user/check_auth');
    },

    // 获取用户资料
    getUserProfile() {
        return apiClient.get('/user/profile');
    },

    // 更新用户名
    updateUsername(newUsername) {
        return apiClient.post('/user/update_username', { newUsername });
    },

    // 更新密码
    updatePassword(currentPassword, newPassword) {
        return apiClient.post('/user/update_password', {
            currentPassword,
            newPassword
        });
    }
};

export const submissionApi = {
    // 获取提交状态
    getSubmission(submissionId) {
        return apiClient.get(`/submission/${submissionId}`);
    },

    // 获取日志
    getSubmissionLog(submissionId) {
        return apiClient.get(`/submission/${submissionId}/log`);
    },

    // 获取波形
    getSubmissionWaveform(submissionId) {
        return apiClient.get(`/submission/${submissionId}/waveform`);
    },

    // 获取用户历史提交记录
    getUserSubmissions() {
        return apiClient.get('/submission');
    }
};
export const aiApi = {
    // 获取AI分析结果
    getAnalysis(submissionId) {
        return apiClient.get(`/ai/analyze/${submissionId}`, {
            timeout: 30000,  // 由于AI分析可能需要较长时间，设置较长的超时
            headers: {
                'Accept': 'application/json'
            }
        });
    }
};

export const adminApi = {
    // 获取所有用户
    getUsers() {
        return apiClient.get('/admin/user');
    },

    // 更新用户信息
    updateUser(userId, userData) {
        return apiClient.put(`/admin/user/${userId}`, userData);
    },

    // 删除用户
    deleteUser(userId) {
        return apiClient.delete(`/admin/user/${userId}`);
    },

    // 获取所有题目
    getProblems() {
        return apiClient.get('/admin/problem');
    },

    // 更新题目信息
    updateProblem(problemId, problemData) {
        return apiClient.put(`/admin/problem/${problemId}`, problemData);
    },

    // 删除题目
    deleteProblem(problemId) {
        return apiClient.delete(`/admin/problem/${problemId}`);
    }
};

export const learningPathApi = {
    // 获取所有学习路径
    getPaths() {
        return apiClient.get('/learningPath/all');
    },
    // 获取单个学习路径信息
    getPath(pathId) {
        return apiClient.get(`/learningPath/${pathId}`);
    },
    // 获取学习路径的题目链
    getPathChain(pathId) {
        return apiClient.get(`/learningPath/${pathId}/chain`);
    }
};

export default {
    problem: problemApi,
    user: userApi,
    submission: submissionApi,
    ai: aiApi,
    admin: adminApi,
    learningPath: learningPathApi
};