<script setup>
import { computed } from 'vue';  // 添加 computed 导入
const props = defineProps({
  content: {
    type: String,
    default: ''
  }
});

// 处理日志内容，添加高亮
const formattedLog = computed(() => {
  if (!props.content) return '';
  
  // 将日志按行分割
  return props.content.split('\n').map(line => {
    // 处理 ERROR 信息
    if (line.includes('ERROR') || line.includes('FAIL') || line.includes('失败')) {
      return `<span class="log-error">${line}</span>`;
    }
    // 处理 INFO 信息
    else if (line.includes('INFO') || line.includes('信息')) {
      return `<span class="log-info">${line}</span>`;
    }
    // 处理 PASS 或成功信息
    else if (line.includes('PASS') || line.includes('SUCCESS') || line.includes('成功')) {
      return `<span class="log-success">${line}</span>`;
    }
    // 处理时间戳
    else if (line.match(/\d{2}:\d{2}:\d{2}/)) {
      return `<span class="log-timestamp">${line}</span>`;
    }
    // 处理警告信息
    else if (line.includes('WARNING') || line.includes('WARN') || line.includes('警告')) {
      return `<span class="log-warning">${line}</span>`;
    }
    return line;
  }).join('\n');
});
</script>

<template>
  <div class="log-viewer">
    <pre v-if="content" v-html="formattedLog" class="log-content"></pre>
    <p v-else class="log-empty text-secondary">暂无日志</p>
  </div>
</template>

<style scoped>
.log-viewer {
  width: 100%;
  font-family: Consolas, 'Courier New', Monaco, monospace;
  font-size: 14px;
}

.log-content {
  background-color: var(--background-color);
  font-family: Consolas, 'Courier New', Monaco, monospace;
  color: var(--text-primary);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid var(--border-color);
}

.log-empty {
  text-align: center;
  padding: var(--spacing-lg);
  background-color: var(--surface-color);
  border-radius: var(--radius-md);
  margin: 0;
}

:deep(.log-error) {
  color: var(--error-color);
  font-weight: 500;
  display: block;
  padding: 2px 0;
}

:deep(.log-info) {
  color: var(--info-color);
  display: block;
  padding: 2px 0;
}

:deep(.log-success) {
  color: var(--success-color);
  font-weight: 500;
  display: block;
  padding: 2px 0;
}

:deep(.log-warning) {
  color: var(--warning-color);
  display: block;
  padding: 2px 0;
}

:deep(.log-timestamp) {
  color: var(--text-secondary);
}

/* 滚动条样式继承自主题 */
.log-content::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.log-content::-webkit-scrollbar-track {
  background: var(--surface-color);
  border-radius: var(--radius-sm);
}

.log-content::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: var(--radius-sm);
}

.log-content::-webkit-scrollbar-thumb:hover {
  background: var(--text-disabled);
}
</style>