<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { problemApi } from '../api';

const router = useRouter();

const problems = ref([]);
const loading = ref(false);
const error = ref(null);

const navigateToProblem = (id) => {
    router.push(`/problem/${id}`);
};

const fetchProblems = async () => {
    loading.value = true;
    error.value = null;

    try {
        const response = await problemApi.getProblems();
        problems.value = response.data.map(problem => ({
            ...problem
        }));
    } catch (err) {
        console.error('获取题目列表失败:', err);
        error.value = err.message || '获取题目失败';
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    fetchProblems();
});

const difficultyColor = (difficulty) => {
    switch (difficulty) {
        case '简单': return 'green';
        case '中等': return 'orange';
        case '困难': return 'red';
        default: return 'black';
    }
};

const completedColor = (is_completed) => {
    switch (is_completed) {
        case '未完成': return 'gray';
        case '已完成': return 'green';
        case   '失败': return 'red';
        case '运行中': return 'gray';
        default: return 'black';
    }
};
</script>

<template>
    <div class="problem-list container">
        <h1 class="text-primary">题目列表</h1>
        <div class="filters">
            <!-- 这里可以添加筛选器，如难度筛选等 -->
        </div>

        <div v-if="loading" class="loading text-secondary flex items-center justify-center">
            加载中...
        </div>

        <div v-else-if="error" class="error card">
            <p class="text-error">加载出错: {{ error }}</p>
            <button @click="fetchProblems" class="button">重试</button>
        </div>

        <table v-else class="problem-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>题目名称</th>
                    <th>难度</th>
                    <th>状态</th>
                    <th>通过/提交</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="problem in problems" :key="problem.id" class="problem-item">
                    <td>{{ problem.id }}</td>
                    <td class="text-primary">{{ problem.title }}</td>
                    <td :style="{ color: difficultyColor(problem.difficulty) }">{{ problem.difficulty }}</td>
                    <td :style="{ color: completedColor(problem.is_completed)}">{{ problem.is_completed}}</td>
                    <td class="text-secondary">{{`${problem.passed_users_count.toString()} / ${problem.submitted_users_count.toString()}`}}</td>
                    <td>
                        <button @click="navigateToProblem(problem.id)" class="button">开始解题</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style scoped>
.problem-list {
    padding: var(--spacing-lg);
}

h1 {
    margin-bottom: var(--spacing-xl);
}

.problem-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: var(--spacing-lg);
    background-color: var(--background-color);
    border-radius: var(--radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

th,
td {
    padding: var(--spacing-md);
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

thead {
    background-color: var(--surface-color);
    border-bottom: 2px solid var(--border-color);
}

th {
    font-weight: 500;
    color: var(--text-primary);
}

.problem-item {
    cursor: pointer;
    transition: background-color var(--transition-fast);
}

.problem-item:hover {
    background-color: var(--surface-color);
}

.loading,
.error {
    padding: var(--spacing-xl);
    text-align: center;
}

.error {
    margin-top: var(--spacing-lg);
}

.error button {
    margin-top: var(--spacing-md);
    background-color: var(--error-color);
}

.error button:hover {
    background-color: color-mix(in srgb, var(--error-color) 80%, black);
}

@media (max-width: 768px) {
    .problem-table {
        font-size: 0.9em;
    }

    th,
    td {
        padding: var(--spacing-sm);
    }

    .button {
        padding: var(--spacing-xs) var(--spacing-sm);
        font-size: 0.9em;
    }
}
</style>
