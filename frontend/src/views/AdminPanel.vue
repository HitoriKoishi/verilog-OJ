<script setup>
import { ref, onMounted, inject } from 'vue';
import { useRouter } from 'vue-router';
import { adminApi } from '../api';
import message from '../utils/message';
import confirm from '../utils/confirm';

const router = useRouter();
const { isLoggedIn, currentUser } = inject('auth');

const activeTab = ref('users');
const users = ref([]);
const problems = ref([]);
const loading = ref(false);
const error = ref(null);

const fetchUsers = async () => {
    loading.value = true;
    try {
        const response = await adminApi.getUsers();
        users.value = response.data;
    } catch (err) {
        message.error(err.response?.data?.message || err.message || '获取用户列表失败');
    } finally {
        loading.value = false;
    }
};

const fetchProblems = async () => {
    loading.value = true;
    try {
        const response = await adminApi.getProblems();
        problems.value = response.data;
    } catch (err) {
        message.error(err.response?.data?.message || err.message || '获取题目列表失败');
    } finally {
        loading.value = false;
    }
};

const updateUser = async (user) => {
    try {
        await adminApi.updateUser(user.id, user);
        await fetchUsers();
        message.success('用户信息更新成功');
    } catch (err) {
        message.error(err.response?.data?.message || err.message || '更新用户信息失败');
    }
};

const deleteUser = async (userId, username) => {
    const confirmed = await confirm({
        title: '删除用户',
        message: `确定要删除用户 "${username}" 吗？此操作不可恢复。`,
        confirmText: '删除',
        cancelText: '取消'
    });
    
    if (!confirmed) return;
    
    try {
        await adminApi.deleteUser(userId);
        await fetchUsers();
        message.success('用户删除成功');
    } catch (err) {
        message.error(err.response?.data?.message || err.message || '删除用户失败');
    }
};

const updateProblem = async (problem) => {
    try {
        await adminApi.updateProblem(problem.id, problem);
        await fetchProblems();
        message.success('题目信息更新成功');
    } catch (err) {
        message.error(err.response?.data?.message || err.message || '更新题目信息失败');
    }
};

const deleteProblem = async (problemId, title) => {
    const confirmed = await confirm({
        title: '删除题目',
        message: `确定要删除题目 "${title}" 吗？此操作不可恢复。`,
        confirmText: '删除',
        cancelText: '取消'
    });
    
    if (!confirmed) return;
    
    try {
        await adminApi.deleteProblem(problemId);
        await fetchProblems();
        message.success('题目删除成功');
    } catch (err) {
        message.error(err.response?.data?.message || err.message || '删除题目失败');
    }
};

onMounted(async () => {
    if (!isLoggedIn.value || !currentUser.value?.is_admin) {
        router.push('/');
        return;
    }
    await fetchUsers();
    await fetchProblems();
});
</script>

<template>
    <div class="admin-panel container">
        <h1 class="text-primary">管理员面板</h1>
        
        <div class="tabs">
            <button 
                :class="['tab-button', { active: activeTab === 'users' }]"
                @click="activeTab = 'users'"
            >
                用户管理
            </button>
            <button 
                :class="['tab-button', { active: activeTab === 'problems' }]"
                @click="activeTab = 'problems'"
            >
                题目管理
            </button>
        </div>

        <div v-if="loading" class="loading">
            加载中...
        </div>

        <div v-else-if="error" class="error">
            {{ error }}
        </div>

        <div v-else>
            <!-- 用户管理面板 -->
            <div v-if="activeTab === 'users'" class="users-panel">
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>用户名</th>
                            <th>邮箱</th>
                            <th>管理员</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="user in users" :key="user.id">
                            <td>{{ user.id }}</td>
                            <td>
                                <input v-model="user.username" @change="updateUser(user)" />
                            </td>
                            <td>
                                <input v-model="user.email" @change="updateUser(user)" />
                            </td>
                            <td>
                                <input 
                                    type="checkbox" 
                                    v-model="user.is_admin" 
                                    @change="updateUser(user)"
                                />
                            </td>
                            <td>
                                <button 
                                    class="delete-button"
                                    @click="deleteUser(user.id, user.username)"
                                >
                                    删除
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- 题目管理面板 -->
            <div v-if="activeTab === 'problems'" class="problems-panel">
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>标题</th>
                            <th>难度</th>
                            <th>标签</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="problem in problems" :key="problem.id">
                            <td>{{ problem.id }}</td>
                            <td>
                                <input v-model="problem.title" @change="updateProblem(problem)" />
                            </td>
                            <td>
                                <select v-model="problem.difficulty" @change="updateProblem(problem)">
                                    <option>简单</option>
                                    <option>中等</option>
                                    <option>困难</option>
                                </select>
                            </td>
                            <td>
                                <input v-model="problem.tags" @change="updateProblem(problem)" />
                            </td>
                            <td>
                                <button 
                                    class="delete-button"
                                    @click="deleteProblem(problem.id, problem.title)"
                                >
                                    删除
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<style scoped>
.admin-panel {
    padding: var(--spacing-lg);
}

.tabs {
    margin-bottom: var(--spacing-lg);
    display: flex;
    gap: var(--spacing-sm);
}

.tab-button {
    padding: var(--spacing-sm) var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: var(--surface-color);
    color: var(--text-primary);
    cursor: pointer;
}

.tab-button.active {
    background: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
}

.admin-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: var(--spacing-md);
}

.admin-table th,
.admin-table td {
    padding: var(--spacing-sm);
    border: 1px solid var(--border-color);
    text-align: left;
}

.admin-table th {
    background: var(--surface-color);
    font-weight: 500;
}

.admin-table input,
.admin-table select {
    width: 100%;
    padding: var(--spacing-xs);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: var(--background-color);
    color: var(--text-primary);
}

.delete-button {
    padding: var(--spacing-xs) var(--spacing-sm);
    background: var(--error-color);
    color: white;
    border: none;
    border-radius: var(--radius-sm);
    cursor: pointer;
}

.delete-button:hover {
    background: color-mix(in srgb, var(--error-color) 80%, black);
}

.loading,
.error {
    text-align: center;
    padding: var(--spacing-lg);
}

.error {
    color: var(--error-color);
}

@media (max-width: 768px) {
    .admin-table {
        font-size: 0.9em;
    }

    .admin-table th,
    .admin-table td {
        padding: var(--spacing-xs);
    }
}
</style> 