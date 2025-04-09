<template>
  <div class="problem-detail">
    <div class="problem-header">
      <h1>{{ problem.title }}</h1>
      <div class="problem-meta">
        <span class="difficulty" :class="problem.difficulty">{{ difficultyText }}</span>
        <span class="submission-count">提交次数: {{ problem.submission_count }}</span>
        <span class="acceptance-rate">通过率: {{ acceptanceRate }}%</span>
      </div>
    </div>
    
    <div class="problem-content">
      <div class="problem-description">
        <h2>题目描述</h2>
        <div v-html="problem.description"></div>
        
        <h2>输入说明</h2>
        <div v-html="problem.input_description"></div>
        
        <h2>输出说明</h2>
        <div v-html="problem.output_description"></div>
        
        <h2>示例</h2>
        <div v-for="(example, index) in problem.examples" :key="index" class="example">
          <h3>示例 {{ index + 1 }}</h3>
          <div class="example-wrapper">
            <div class="example-input">
              <h4>输入</h4>
              <pre>{{ example.input }}</pre>
            </div>
            <div class="example-output">
              <h4>输出</h4>
              <pre>{{ example.output }}</pre>
            </div>
          </div>
          <div class="example-explanation" v-if="example.explanation">
            <h4>解释</h4>
            <div v-html="example.explanation"></div>
          </div>
        </div>
        
        <h2>限制</h2>
        <ul class="constraints">
          <li>时间限制: {{ problem.time_limit }} 秒</li>
          <li>内存限制: {{ problem.memory_limit }} MB</li>
        </ul>
      </div>
      
      <div class="code-editor">
        <h2>代码编辑器</h2>
        <div class="editor-toolbar">
          <button @click="submitCode" :disabled="isSubmitting">{{ isSubmitting ? '提交中...' : '提交代码' }}</button>
        </div>
        
        <div class="monaco-editor-container" ref="editorContainer"></div>
        
        <div class="submission-result" v-if="submissionResult">
          <h3>评测结果: <span :class="submissionResult.status">{{ submissionResult.status }}</span></h3>
          <div v-if="submissionResult.error" class="error-message">
            <pre>{{ submissionResult.error }}</pre>
          </div>
          <div v-if="submissionResult.execution_time" class="execution-stats">
            执行时间: {{ submissionResult.execution_time.toFixed(2) }} ms
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import * as monaco from 'monaco-editor';

export default {
  name: 'ProblemDetail',
  
  setup() {
    const route = useRoute();
    const problem = ref({
      title: '',
      difficulty: 'medium',
      submission_count: 0,
      accepted_count: 0,
      description: '',
      input_description: '',
      output_description: '',
      examples: [],
      time_limit: 1,
      memory_limit: 256
    });
    
    const editor = ref(null);
    const editorContainer = ref(null);
    const code = ref('');
    const isSubmitting = ref(false);
    const submissionResult = ref(null);
    
    const difficultyText = computed(() => {
      const map = {
        'easy': '简单',
        'medium': '中等',
        'hard': '困难'
      };
      return map[problem.value.difficulty] || '中等';
    });
    
    const acceptanceRate = computed(() => {
      if (problem.value.submission_count === 0) return 0;
      return ((problem.value.accepted_count / problem.value.submission_count) * 100).toFixed(1);
    });
    
    const fetchProblem = async () => {
      try {
        const response = await axios.get(`/api/problems/${route.params.id}/`);
        problem.value = response.data;
      } catch (error) {
        console.error('获取题目失败', error);
      }
    };
    
    const initEditor = () => {
      if (editorContainer.value) {
        editor.value = monaco.editor.create(editorContainer.value, {
          value: '// 请在此编写您的Verilog代码\nmodule solution(\n  // TODO: 定义您的模块接口\n);\n\n  // TODO: 实现模块功能\n\nendmodule',
          language: 'verilog',
          theme: 'vs-dark',
          automaticLayout: true,
          minimap: { enabled: false }
        });
        
        editor.value.onDidChangeModelContent(() => {
          code.value = editor.value.getValue();
        });
      }
    };
    
    const submitCode = async () => {
      if (!code.value.trim()) return;
      
      isSubmitting.value = true;
      submissionResult.value = null;
      
      try {
        const response = await axios.post('/api/submissions/', {
          problem_id: route.params.id,
          code: code.value,
          language: 'verilog'
        });
        
        // 轮询检查评测结果
        checkSubmissionResult(response.data.id);
      } catch (error) {
        console.error('提交代码失败', error);
        isSubmitting.value = false;
      }
    };
    
    const checkSubmissionResult = async (submissionId) => {
      try {
        const response = await axios.get(`/api/submissions/${submissionId}/`);
        if (response.data.status === 'PENDING' || response.data.status === 'RUNNING') {
          // 继续轮询
          setTimeout(() => checkSubmissionResult(submissionId), 1000);
        } else {
          // 评测完成
          submissionResult.value = response.data;
          isSubmitting.value = false;
        }
      } catch (error) {
        console.error('获取评测结果失败', error);
        isSubmitting.value = false;
      }
    };
    
    onMounted(() => {
      fetchProblem();
      initEditor();
    });
    
    onUnmounted(() => {
      if (editor.value) {
        editor.value.dispose();
      }
    });
    
    return {
      problem,
      difficultyText,
      acceptanceRate,
      editorContainer,
      submitCode,
      isSubmitting,
      submissionResult
    };
  }
}
</script>

<style scoped>
.problem-detail {
  display: flex;
  flex-direction: column;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.problem-header {
  margin-bottom: 20px;
}

.problem-meta {
  display: flex;
  gap: 15px;
}

.difficulty {
  padding: 3px 8px;
  border-radius: 4px;
  font-weight: bold;
}

.difficulty.easy {
  background-color: #00af9b;
  color: white;
}

.difficulty.medium {
  background-color: #ffb800;
  color: black;
}

.difficulty.hard {
  background-color: #ff2d55;
  color: white;
}

.problem-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.monaco-editor-container {
  height: 500px;
  border: 1px solid #ccc;
}

.example {
  margin-bottom: 20px;
}

.example-wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.submission-result {
  margin-top: 20px;
  padding: 15px;
  border-radius: 4px;
  background-color: #f5f5f5;
}

.error-message {
  max-height: 200px;
  overflow: auto;
  background-color: #ffeaea;
  padding: 10px;
  border-radius: 4px;
}

.ACCEPTED {
  color: #00af9b;
}

.WRONG_ANSWER, .COMPILE_ERROR, .RUNTIME_ERROR, .TIME_LIMIT_EXCEEDED {
  color: #ff2d55;
}
</style>
