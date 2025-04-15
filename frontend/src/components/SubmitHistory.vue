<script setup>
import { ref, onMounted } from 'vue';
import { problemApi } from '../api';

const props = defineProps({
  problemId: {
    type: [Number],
    required: true
  }
});

const submissionHistory = ref([]);
const loading = ref(false);
const error = ref(null);

const emit = defineEmits(['select-submission']);

// 格式化日期
const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
};

// 获取状态样式
const getStatusStyle = (status) => {
  switch (status) {
    case 'success':
      return 'text-success';
    case 'failed':
      return 'text-error';
    default:
      return 'text-pending';
  }
};

// 获取提交历史
const fetchSubmitHistory = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await problemApi.getProblemSubmitHistory(props.problemId);
    submissionHistory.value = response.data;
  } catch (err) {
    console.error('获取提交历史失败:', err);
    error.value = err.response?.data?.error || '获取提交历史失败';
  } finally {
    loading.value = false;
  }
};

// 组件挂载时获取历史记录
onMounted(() => {
  fetchSubmitHistory();
});

// 暴露刷新方法
defineExpose({
  refresh: fetchSubmitHistory
});

// 添加点击处理函数
const handleSubmissionClick = (submission) => {
  emit('select-submission', submission.submission_id);
};
</script>

<template>
  <div class="submit-history card">
    <h3 class="text-primary">提交历史</h3>
    
    <div v-if="loading" class="loading text-secondary">
      加载中...
    </div>
    
    <div v-else-if="error" class="error text-error">
      {{ error }}
    </div>
    
    <div v-else-if="submissionHistory.length === 0" class="empty text-disabled">
      暂无提交记录
    </div>
    
    <div v-else class="history-list">
      <div v-for="submission in submissionHistory" 
           :key="submission.submission_id" 
           class="history-item"
           @click="handleSubmissionClick(submission)"
      >
        <span class="submission-id text-secondary">#{{ submission.submission_id }}</span>
        <span :class="['status', getStatusStyle(submission.status)]">
          {{ submission.status === 'success' ? '通过' : '失败' }}
        </span>
        <span class="time text-secondary">{{ formatDate(submission.created_at) }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.submit-history {
  margin-top: var(--spacing-lg);
}

.history-list {
  max-height: 250px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  align-items: center;
  padding: var(--spacing-sm);
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  transition: background-color var(--transition-fast);
}

.history-item:last-child {
  border-bottom: none;
}

.history-item:hover {
  background-color: var(--surface-color);
}

.submission-id {
  flex: 0 0 80px;
}

.status {
  flex: 0 0 60px;
  text-align: center;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: 0.9em;
}

.text-success {
  color: var(--success-color);
  background-color: color-mix(in srgb, var(--success-color) 10%, transparent);
}

.text-error {
  color: var(--error-color);
  background-color: color-mix(in srgb, var(--error-color) 10%, transparent);
}

.text-pending {
  color: var(--warning-color);
  background-color: color-mix(in srgb, var(--warning-color) 10%, transparent);
}

.time {
  flex: 1;
  text-align: right;
  font-size: 0.9em;
}

.loading, .error, .empty {
  text-align: center;
  padding: var(--spacing-lg);
}
</style>