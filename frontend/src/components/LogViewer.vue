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
    <p v-else class="log-empty">暂无日志</p>
  </div>
</template>

<style scoped>
.log-viewer {
  width: 100%;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 14px;
}

.log-content {
  background-color: #1e1e1e;
  font-family: 'Consolas', 'Monaco', monospace;
  color: #d4d4d4;
  padding: 16px;
  border-radius: 6px;
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 400px;
  overflow-y: auto;
}

.log-empty {
  text-align: center;
  padding: 40px;
  color: #666;
  background: #f5f5f500;
  border-radius: 6px;
}

:deep(.log-error) {
  color: #ff6464;
  font-weight: 500;
  display: block;
  padding: 2px 0;
}

:deep(.log-info) {
  color: #64b5f6;
  display: block;
  padding: 2px 0;
}

:deep(.log-success) {
  color: #81c784;
  font-weight: 500;
  display: block;
  padding: 2px 0;
}

:deep(.log-warning) {
  color: #ffb74d;
  display: block;
  padding: 2px 0;
}

:deep(.log-timestamp) {
  color: #9e9e9e;
}

/* 滚动条样式 */
.log-content::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.log-content::-webkit-scrollbar-track {
  background: #2e2e2e;
  border-radius: 4px;
}

.log-content::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 4px;
}

.log-content::-webkit-scrollbar-thumb:hover {
  background: #666;
}

/* 暗色主题支持 */
@media (prefers-color-scheme: light) {
  .log-content {
    background-color: #f8f8f800;
    color: #333;
  }

  :deep(.log-error) {
    color: #d32f2f;
  }

  :deep(.log-info) {
    color: #1976d2;
  }

  :deep(.log-success) {
    color: #388e3c;
  }

  :deep(.log-warning) {
    color: #f57c00;
  }

  :deep(.log-timestamp) {
    color: #616161;
  }

  .log-content::-webkit-scrollbar-track {
    background: #eee;
  }

  .log-content::-webkit-scrollbar-thumb {
    background: #ccc;
  }

  .log-content::-webkit-scrollbar-thumb:hover {
    background: #bbb;
  }
}
</style>