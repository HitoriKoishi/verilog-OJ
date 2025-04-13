<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
<<<<<<< Updated upstream
import { problemApi } from '../api';

const router = useRouter();

const problems = ref([]);
=======

const router = useRouter();

// 使用静态数据
// const problems = ref([
//   { id: 1, title: '简单异或触发器', difficulty: '简单', completed: false },
//   { id: 2, title: '3输入与非门', difficulty: '简单', completed: false },
//   { id: 3, title: '三人表决器', difficulty: '中等', completed: false },
//   { id: 4, title: 'JK触发器', difficulty: '中等', completed: false },
//   { id: 5, title: '基本D触发器', difficulty: '中等', completed: false },
//   { id: 6, title: '四bit十进制计数器', difficulty: '困难', completed: false }
// ]);

const problems = ref([]);

>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
        problems.value = response.data.map(problem => ({
            ...problem
        }));
=======
        problems.value = response.data;
>>>>>>> Stashed changes
    } catch (err) {
        console.error('获取题目列表失败:', err);
        error.value = err.message || '获取题目失败';
    } finally {
        loading.value = false;
    }
};

<<<<<<< Updated upstream
onMounted(() => {
    fetchProblems();
});

=======
>>>>>>> Stashed changes
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
    <div class="problem-list">
        <h1>题目列表</h1>
        <div class="filters">
            <!-- 这里可以添加筛选器，如难度筛选等 -->
        </div>

        <div v-if="loading" class="loading">
            加载中...
        </div>

        <div v-else-if="error" class="error">
            <p>加载出错: {{ error }}</p>
<<<<<<< Updated upstream
            <button @click="fetchProblems">重试</button>
=======
            <button @click="store.dispatch('problems/fetchProblems')">重试</button>
>>>>>>> Stashed changes
        </div>

        <table v-else>
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
                    <td>{{ problem.title }}</td>
                    <td :style="{ color: difficultyColor(problem.difficulty) }">{{ problem.difficulty }}</td>
                    <td :style="{ color: completedColor(problem.is_completed)}">{{ problem.is_completed}}</td>
                    <td>{{`${problem.passed_users_count.toString()} / ${problem.submitted_users_count.toString()}`}}</td>
                    <td>
                        <button @click="navigateToProblem(problem.id)" class="solve-btn">开始解题</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style scoped>
.problem-list {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

h1 {
    margin-bottom: 20px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th,
td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

thead {
    background-color: #f2f2f2;
}

.problem-item {
    cursor: pointer;
}

.problem-item:hover {
    background-color: #f5f5f5;
}

.solve-btn {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
}

.solve-btn:hover {
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

.error button {
    margin-top: 10px;
    background-color: #f44336;
    color: white;
}
</style>
