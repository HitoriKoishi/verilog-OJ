<script setup>
import { ref, onMounted, onUnmounted, shallowRef } from 'vue';
import { EditorState } from '@codemirror/state';
import { EditorView } from '@codemirror/view';
import { basicSetup } from 'codemirror';
import { StreamLanguage } from '@codemirror/language';
import { verilog } from '@codemirror/legacy-modes/mode/verilog';

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '// 在此处编写Verilog代码'
  }
});

const emit = defineEmits(['update:modelValue', 'change']);

const editorElement = ref(null);
const editorView = shallowRef(null);

const updateEditorContent = (content) => {
  if (!editorView.value) return;
  const transaction = editorView.value.state.update({
    changes: {
      from: 0,
      to: editorView.value.state.doc.length,
      insert: content
    }
  });
  editorView.value.dispatch(transaction);
};

const initEditor = async () => {
  if (!editorElement.value) {
    console.error('编辑器容器元素不存在');
    return;
  }

  try {
    if (editorView.value) {
      editorView.value.destroy();
    }

    editorElement.value.innerHTML = '';

    const startState = EditorState.create({
      doc: props.modelValue || props.placeholder,
      extensions: [
        basicSetup,
        StreamLanguage.define(verilog),
        EditorView.theme({
          "&": {
            fontSize: "14px",
            height: "100%"
          },
          ".cm-content": {
            fontFamily: "'Consolas', 'Monaco', monospace"
          },
          ".cm-gutters": {
            backgroundColor: "#f5f5f5",
            borderRight: "1px solid #ddd"
          }
        }),
        EditorView.updateListener.of(update => {
          if (update.docChanged) {
            const content = update.state.doc.toString();
            emit('update:modelValue', content);
            emit('change', content);
          }
        })
      ]
    });

    editorView.value = new EditorView({
      state: startState,
      parent: editorElement.value
    });

  } catch (err) {
    console.error('初始化编辑器失败:', err);
    editorElement.value.innerHTML = `<div style="color:red; padding:10px;">
      编辑器加载失败: ${err.message}
      <br>
      <button onclick="location.reload()">刷新页面重试</button>
    </div>`;
  }
};

// 对外暴露的方法
defineExpose({
  updateContent: updateEditorContent,
  clearContent: () => updateEditorContent('')
});

onMounted(() => {
  initEditor();
});

onUnmounted(() => {
  if (editorView.value) {
    editorView.value.destroy();
  }
});
</script>

<template>
  <div class="verilog-editor">
    <div ref="editorElement" class="editor-container"></div>
  </div>
</template>

<style scoped>
.verilog-editor {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.editor-container {
  flex: 1;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  overflow: hidden;
  background-color: var(--background-color);
  font-family: var(--font-family-code);
}

.editor-container :deep(.cm-editor) {
  height: 100%;
  width: 100%;
  background-color: var(--background-color);
}

.editor-container :deep(.cm-scroller) {
  font-family: var(--font-family-code);
}

.editor-container :deep(.cm-content) {
  padding: var(--spacing-xs);
  color: var(--text-primary);
}

.editor-container :deep(.cm-line) {
  padding: 0 var(--spacing-xs);
}

.editor-container :deep(.cm-gutters) {
  background-color: var(--surface-color);
  border-right: 1px solid var(--border-color);
  color: var(--text-secondary);
}

.editor-container :deep(.cm-activeLineGutter) {
  background-color: var(--surface-color);
  color: var(--text-primary);
}

.editor-container :deep(.cm-selectionBackground) {
  background-color: var(--primary-color);
  opacity: 0.2;
}

.editor-container :deep(.cm-focused) {
  outline: none;
}

.editor-container :deep(.cm-cursor) {
  border-left-color: var(--primary-color);
}

/* 滚动条样式 */
.editor-container :deep(.cm-scroller::-webkit-scrollbar) {
  width: 8px;
  height: 8px;
}

.editor-container :deep(.cm-scroller::-webkit-scrollbar-track) {
  background: var(--surface-color);
  border-radius: var(--radius-sm);
}

.editor-container :deep(.cm-scroller::-webkit-scrollbar-thumb) {
  background: var(--border-color);
  border-radius: var(--radius-sm);
}

.editor-container :deep(.cm-scroller::-webkit-scrollbar-thumb:hover) {
  background: var(--text-disabled);
}
</style>