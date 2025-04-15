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
  color: var(--text-primary);
  line-height: 1.6;
}

.markdown-content :deep(img) {
  max-width: 60%;
  height: auto;
  display: block;
  margin: var(--spacing-md) auto;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) {
  margin-top: var(--spacing-lg);
  margin-bottom: var(--spacing-sm);
  color: var(--text-primary);
  font-weight: 600;
}

.markdown-content :deep(p) {
  text-indent: 2em;
  margin: var(--spacing-sm) 0;
  color: var(--text-secondary);
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  padding-left: 2em;
  margin: var(--spacing-sm) 0;
  color: var(--text-secondary);
}

.markdown-content :deep(li) {
  margin: var(--spacing-xs) 0;
}

.markdown-content :deep(ul ul),
.markdown-content :deep(ul ol),
.markdown-content :deep(ol ul),
.markdown-content :deep(ol ol) {
  margin: var(--spacing-xs) 0;
}

.markdown-content :deep(pre) {
  background-color: var(--surface-color);
  padding: var(--spacing-md);
  border-radius: var(--radius-sm);
  overflow-x: auto;
  border: 1px solid var(--border-color);
  margin: var(--spacing-md) 0;
}

.markdown-content :deep(code) {
  font-family: var(--font-family-code);
  background-color: var(--surface-color);
  padding: 2px var(--spacing-xs);
  border-radius: var(--radius-sm);
  font-size: 0.9em;
  color: var(--primary-color);
}

.markdown-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: var(--spacing-md) 0;
  background-color: var(--background-color);
  border-radius: var(--radius-sm);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.markdown-content :deep(th),
.markdown-content :deep(td) {
  border: 1px solid var(--border-color);
  padding: var(--spacing-sm);
  text-align: left;
}

.markdown-content :deep(th) {
  background-color: var(--surface-color);
  font-weight: 500;
  color: var(--text-primary);
}

.markdown-content :deep(td) {
  color: var(--text-secondary);
}

.markdown-content :deep(blockquote) {
  margin: var(--spacing-md) 0;
  padding: var(--spacing-sm) var(--spacing-md);
  border-left: 4px solid var(--primary-color);
  background-color: var(--surface-color);
  color: var(--text-secondary);
  font-style: italic;
}

.markdown-content :deep(hr) {
  border: none;
  border-top: 1px solid var(--border-color);
  margin: var(--spacing-lg) 0;
}

.markdown-content :deep(a) {
  color: var(--primary-color);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.markdown-content :deep(a:hover) {
  color: var(--primary-hover);
  text-decoration: underline;
}
</style>