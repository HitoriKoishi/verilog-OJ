<script setup>
import { computed } from 'vue';
import { marked } from 'marked';

const props = defineProps({
  content: {
    type: String,
    required: true
  },
  removeFirstH1: {
    type: Boolean,
    default: true
  }
});

const renderedContent = computed(() => {
  if (!props.content) return '<p>没有内容</p>';

  let processedContent = props.content;
  
  if (props.removeFirstH1) {
    // 移除第一个一级标题
    const lines = props.content.split('\n');
    let firstH1Index = lines.findIndex(line => line.startsWith('# '));
    
    if (firstH1Index !== -1) {
      processedContent = lines.slice(firstH1Index + 1).join('\n');
    }
  }

  // 设置 marked 选项
  const renderer = new marked.Renderer();
  marked.setOptions({
    renderer: renderer,
    gfm: true,
    breaks: true,
    sanitize: false,
    smartLists: true,
    smartypants: false,
    xhtml: false
  });

  return marked(processedContent);
});
</script>

<template>
  <div class="markdown-content" v-html="renderedContent"></div>
</template>

<style scoped>
.markdown-content {
  color: #333;
}

.markdown-content :deep(img) {
  max-width: 60%;
  height: auto;
  display: block;
  margin: 15px auto;
  border-radius: 4px;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) {
  margin-top: 1em;
  margin-bottom: 0.5em;
}

.markdown-content :deep(p) {
  text-indent: 2em;
  margin: 0.5em 0;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  padding-left: 2em;
  margin: 0.5em 0;
}

.markdown-content :deep(li) {
  margin: 0.3em 0;
}

.markdown-content :deep(ul ul),
.markdown-content :deep(ul ol),
.markdown-content :deep(ol ul),
.markdown-content :deep(ol ol) {
  margin: 0.2em 0;
}

.markdown-content :deep(pre) {
  background-color: #f5f5f5;
  padding: 12px;
  border-radius: 4px;
  overflow-x: auto;
}

.markdown-content :deep(code) {
  font-family: 'Consolas', 'Monaco', monospace;
  background-color: #f0f0f0;
  padding: 2px 4px;
  border-radius: 3px;
  font-size: 0.9em;
}

.markdown-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}

.markdown-content :deep(th),
.markdown-content :deep(td) {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.markdown-content :deep(th) {
  background-color: #f2f2f2;
}

/* 暗色主题支持 */
@media (prefers-color-scheme: dark) {
  .markdown-content {
    color: #e0e0e0;
  }

  .markdown-content :deep(pre) {
    background-color: #2d2d2d;
  }

  .markdown-content :deep(code) {
    background-color: #2d2d2d;
  }

  .markdown-content :deep(th),
  .markdown-content :deep(td) {
    border-color: #444;
  }

  .markdown-content :deep(th) {
    background-color: #2d2d2d;
  }
}
</style>