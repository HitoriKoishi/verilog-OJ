<script setup>
import { ref, onMounted, onUnmounted, shallowRef, watch } from 'vue';
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
  },
  isDarkMode: {
    type: Boolean,
    default: false
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

const getThemeExtension = (isDark) => {
  return EditorView.theme({
    "&": {
      fontSize: "14px",
      height: "100%"
    },
    ".cm-content": {
      fontFamily: "'Consolas', 'Monaco', monospace",
      color: isDark ? "#e0e0e0" : "inherit"
    },
    ".cm-gutters": {
      backgroundColor: isDark ? "#1e1e1e" : "#f5f5f5",
      borderRight: `1px solid ${isDark ? "#333" : "#ddd"}`,
      color: isDark ? "#aaa" : "inherit"
    },
    "&.cm-focused": {
      outline: "none"
    },
    ".cm-line": {
      color: isDark ? "#e0e0e0" : "inherit"
    },
    ".cm-activeLine": {
      backgroundColor: isDark ? "rgba(255, 255, 255, 0.05)" : "rgba(0, 0, 0, 0.05)"
    },
    ".cm-activeLineGutter": {
      backgroundColor: isDark ? "#252525" : "#f0f0f0"
    },
    ".cm-selectionMatch": {
      backgroundColor: isDark ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.1)"
    },
    // 语法高亮颜色
    ".cm-keyword": { color: isDark ? "#cc99cd" : "#708" },
    ".cm-number": { color: isDark ? "#f08d49" : "#164" },
    ".cm-comment": { color: isDark ? "#999" : "#940" },
    ".cm-string": { color: isDark ? "#7ec699" : "#a11" },
    ".cm-property": { color: isDark ? "#66d9ef" : "#00c" },
    ".cm-atom": { color: isDark ? "#f08d49" : "#219" },
    ".cm-variable": { color: isDark ? "#e0e0e0" : "#00c" },
    ".cm-def": { color: isDark ? "#fd971f" : "#00f" }
  });
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
        getThemeExtension(props.isDarkMode),
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

// 监听暗色模式变化并重新初始化编辑器
watch(() => props.isDarkMode, () => {
  initEditor();
});

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
  <div class="verilog-editor" :class="{ 'dark-theme': isDarkMode }">
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
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
  background-color: #ffffff;
}

.editor-container :deep(.cm-editor) {
  height: 100%;
  width: 100%;
}

.editor-container :deep(.cm-scroller) {
  overflow: auto;
  font-family: 'Consolas', 'Monaco', monospace;
}

.editor-container :deep(.cm-content) {
  font-family: 'Consolas', 'Monaco', monospace;
  padding: 4px;
}

.editor-container :deep(.cm-line) {
  padding: 0 4px;
}

/* 暗色主题样式 */
.dark-theme .editor-container {
  border-color: #333;
  background-color: #1e1e1e;
}

.dark-theme .editor-container :deep(.cm-gutters) {
  background-color: #1e1e1e;
  border-color: #333;
}
</style>