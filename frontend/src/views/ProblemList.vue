<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { problemApi } from '../api';

const router = useRouter();

const problems = ref([]);
const loading = ref(false);
const error = ref(null);
const selectedTags = ref([]);
const allTags = ref([]);

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
        
        // 收集所有唯一的标签
        const tagsSet = new Set();
        problems.value.forEach(problem => {
            problem.tags.forEach(tag => tagsSet.add(tag));
        });
        allTags.value = Array.from(tagsSet);
    } catch (err) {
        console.error('获取题目列表失败:', err);
        error.value = err.message || '获取题目失败';
    } finally {
        loading.value = false;
    }
};

// 根据选中的标签筛选题目
const filteredProblems = computed(() => {
    if (selectedTags.value.length === 0) {
        return problems.value;
    }
    return problems.value.filter(problem => 
        selectedTags.value.every(tag => problem.tags.includes(tag))
    );
});

const toggleTag = (tag) => {
    const index = selectedTags.value.indexOf(tag);
    if (index === -1) {
        selectedTags.value.push(tag);
    } else {
        selectedTags.value.splice(index, 1);
    }
};

onMounted(() => {
    fetchProblems();
});

const difficultyColor = (difficulty) => {
    switch (difficulty) {
        case '简单': return 'var(--success-color)';
        case '中等': return 'var(--warning-color)';
        case '困难': return 'var(--error-color)';
        default: return 'var(--text-primary)';
    }
};

const completedColor = (is_completed) => {
    switch (is_completed) {
        case '未完成': return 'var(--text-disabled)';
        case '已完成': return 'var(--success-color)';
        case '失败': return 'var(--error-color)';
        case '运行中': return 'var(--text-disabled)';
        default: return 'var(--text-primary)';
    }
};

// 修改key生成方式，只使用问题ID
const getItemKey = (problem) => {
    return `problem-${problem.id}`;
};
</script>

<template>
    <div class="problem-list container">
        <h1 class="text-primary">题目列表</h1>
        <div class="filters">
            <div class="tags-filter">
                <h3>标签筛选：</h3>
                <div class="tags-container">
                    <button v-for="tag in allTags" :key="tag" @click="toggleTag(tag)"
                        :class="['tag-button', { active: selectedTags.includes(tag) }]">
                        {{ tag }}
                    </button>
                </div>
            </div>
        </div>

        <div v-if="loading" class="loading text-secondary flex items-center justify-center">
            加载中...
        </div>

        <div v-else-if="error" class="error card">
            <p class="text-error">加载出错: {{ error }}</p>
            <button @click="fetchProblems" class="button">重试</button>
        </div>

        <div v-else class="problem-table-wrapper">
            <table class="problem-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>题目名称</th>
                        <th>标签</th>
                        <th>难度</th>
                        <th>状态</th>
                        <th>通过/提交</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <TransitionGroup name="problem-list" tag="tbody">
                    <tr v-for="problem in filteredProblems" :key="getItemKey(problem)" class="problem-item">
                        <td class="problem-cell">{{ problem.id }}</td>
                        <td class="problem-cell">{{ problem.title }}</td>
                        <td class="problem-cell tags-cell">
                            <span v-for="tag in problem.tags" :key="tag" class="tag-label">
                                {{ tag }}
                            </span>
                        </td>
                        <td class="problem-cell" :style="{ color: difficultyColor(problem.difficulty) }">{{ problem.difficulty }}</td>
                        <td class="problem-cell" :style="{ color: completedColor(problem.is_completed)}">{{ problem.is_completed}}</td>
                        <td class="problem-cell">{{`${problem.passed_users_count.toString()} / ${problem.submitted_users_count.toString()}`}}</td>
                        <td class="problem-cell">
                            <button @click="navigateToProblem(problem.id)" class="button">开始解题</button>
                        </td>
                    </tr>
                </TransitionGroup>
            </table>
        </div>
    </div>
</template>

<style scoped>
.problem-list {
    padding: var(--spacing-lg);
}

h1 {
    margin-bottom: var(--spacing-xl);
}

.filters {
    margin-bottom: var(--spacing-lg);
    padding: var(--spacing-md);
    background-color: var(--surface-color);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
}

.tags-filter h3 {
    margin-bottom: var(--spacing-sm);
    color: var(--text-primary);
    font-size: 1rem;
}

.tags-container {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-xs);
}

.tag-button {
    padding: var(--spacing-xs) var(--spacing-sm);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background-color: var(--background-color);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all var(--transition-fast);
}

.tag-button:hover {
    background-color: var(--surface-color);
    border-color: var(--primary-color);
}

.tag-button.active {
    background-color: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
}

.problem-table {
    width: 100%;
    table-layout: fixed;
    border-collapse: separate;
    border-spacing: 0;
    margin-top: var(--spacing-lg);
    background-color: transparent;
    border-radius: var(--radius-md);
    overflow: visible;
    box-shadow: var(--shadow-sm);
    position: relative;
}

.problem-table tbody {
    position: relative;
    width: 100%;
    display: block;
    min-height: 50px;
}

/* 设置每列的固定宽度 */
.problem-table th:nth-child(1),
.problem-table td:nth-child(1) {
    width: 60px;
}

.problem-table th:nth-child(2),
.problem-table td:nth-child(2) {
    width: 25%;
}

.problem-table th:nth-child(3),
.problem-table td:nth-child(3) {
    width: 25%;
}

.problem-table th:nth-child(4),
.problem-table td:nth-child(4) {
    width: 80px;
}

.problem-table th:nth-child(5),
.problem-table td:nth-child(5) {
    width: 80px;
}

.problem-table th:nth-child(6),
.problem-table td:nth-child(6) {
    width: 100px;
}

.problem-table th:nth-child(7),
.problem-table td:nth-child(7) {
    width: 100px;
}

/* 处理内容溢出 */
.problem-table td {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.tags-cell {
    gap: var(--spacing-xs);
    max-width: 100%;
    overflow: hidden;
    gap: var(--spacing-xs);
}

.tag-label {
    font-size: 0.85em;
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    background-color: var(--surface-color);
    color: var(--text-secondary);
    white-space: nowrap;
    margin-right: var(--spacing-xs);
    margin-bottom: var(--spacing-xs);
    display: inline-block;
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
    display: table;
    width: 100%;
    table-layout: fixed;
}

th {
    font-weight: 500;
    color: var(--text-primary);
}

.problem-item {
    background-color: var(--background-color);
    transition: background-color var(--transition-fast);
    width: 100%;
    display: table;
    table-layout: fixed;
}

.problem-item:hover {
    background-color: var(--surface-color);
}

.problem-cell {
    background-color: inherit;
    display: table-cell;
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

/* 列表项动画 */
.problem-list-enter-active,
.problem-list-leave-active {
    transition: all var(--transition-slow);
}

.problem-list-leave-active {
    position: absolute;
    width: 100%;
    pointer-events: none;
}

.problem-list-enter-from,
.problem-list-leave-to {
    opacity: 0;
    transform: translateY(-30px);
}

.problem-list-move {
    transition: transform var(--transition-slow);
}

/* 确保动画容器正确定位 */
.problem-table-wrapper {
    position: relative;
    margin-bottom: var(--spacing-xl);
}

/* 响应式设计 */
@media (max-width: 768px) {
    .problem-table {
        font-size: 0.9em;
    }

    th,
    td {
        padding: var(--spacing-sm);
    }

    .tag-button {
        font-size: 0.9em;
    }

    .tags-container {
        gap: var(--spacing-xxs);
    }

    /* 移动端调整列宽 */
    .problem-table th:nth-child(1),
    .problem-table td:nth-child(1) {
        width: 40px;
    }

    .problem-table th:nth-child(2),
    .problem-table td:nth-child(2) {
        width: 30%;
    }

    .problem-table th:nth-child(3),
    .problem-table td:nth-child(3) {
        width: 20%;
    }

    .problem-table th:nth-child(4),
    .problem-table td:nth-child(4),
    .problem-table th:nth-child(5),
    .problem-table td:nth-child(5) {
        width: 60px;
    }

    .problem-table th:nth-child(6),
    .problem-table td:nth-child(6),
    .problem-table th:nth-child(7),
    .problem-table td:nth-child(7) {
        width: 80px;
    }
}
</style>
