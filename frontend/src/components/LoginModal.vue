<script setup>
import { ref, inject, watch } from 'vue';

const props = defineProps({
  isRegistering: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close']);

// 引入认证上下文
const { login } = inject('auth');

const username = ref('');
const password = ref('');
const confirmPassword = ref('');
const email = ref('');
const errorMessage = ref('');
const isSubmitting = ref(false);
const mode = ref(props.isRegistering ? 'register' : 'login');

// 监听 isRegistering 属性变化
watch(() => props.isRegistering, (newVal) => {
  mode.value = newVal ? 'register' : 'login';
});

const toggleMode = () => {
  mode.value = mode.value === 'login' ? 'register' : 'login';
  errorMessage.value = '';
};

const validateForm = () => {
  errorMessage.value = '';
  
  if (!username.value) {
    errorMessage.value = '请输入用户名';
    return false;
  }
  
  if (!password.value) {
    errorMessage.value = '请输入密码';
    return false;
  }
  
  if (mode.value === 'register') {
    if (password.value.length < 6) {
      errorMessage.value = '密码长度至少为6位';
      return false;
    }
    
    if (password.value !== confirmPassword.value) {
      errorMessage.value = '两次输入的密码不一致';
      return false;
    }
    
    if (email.value && !/^\S+@\S+\.\S+$/.test(email.value)) {
      errorMessage.value = '邮箱格式不正确';
      return false;
    }
  }
  
  return true;
};

const handleSubmit = async () => {
  if (!validateForm()) return;
  
  isSubmitting.value = true;
  
  try {
    // 这里是模拟登录/注册
    // 实际项目中应该调用API进行身份验证
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    if (mode.value === 'login') {
      // 模拟登录成功
      login({
        username: username.value,
        id: Math.floor(Math.random() * 1000)
      });
    } else {
      // 模拟注册成功后自动登录
      login({
        username: username.value,
        email: email.value,
        id: Math.floor(Math.random() * 1000)
      });
    }
    
    emit('close');
  } catch (error) {
    errorMessage.value = error.message || '发生错误，请重试';
  } finally {
    isSubmitting.value = false;
  }
};

const closeModal = () => {
  emit('close');
};

// 点击遮罩层关闭
const handleOverlayClick = (e) => {
  if (e.target.classList.contains('modal-overlay')) {
    closeModal();
  }
};
</script>

<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-container">
      <div class="modal-header">
        <h2>{{ mode === 'login' ? '用户登录' : '用户注册' }}</h2>
        <button class="close-button" @click="closeModal">&times;</button>
      </div>
      
      <div class="modal-body">
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            placeholder="请输入用户名"
            :disabled="isSubmitting"
          >
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="请输入密码"
            :disabled="isSubmitting"
          >
        </div>
        
        <template v-if="mode === 'register'">
          <div class="form-group">
            <label for="confirmPassword">确认密码</label>
            <input 
              type="password" 
              id="confirmPassword" 
              v-model="confirmPassword" 
              placeholder="请再次输入密码"
              :disabled="isSubmitting"
            >
          </div>
          
          <div class="form-group">
            <label for="email">邮箱（选填）</label>
            <input 
              type="email" 
              id="email" 
              v-model="email" 
              placeholder="请输入邮箱"
              :disabled="isSubmitting"
            >
          </div>
        </template>
      </div>
      
      <div class="modal-footer">
        <button 
          class="submit-button" 
          @click="handleSubmit"
          :disabled="isSubmitting"
        >
          {{ isSubmitting ? '处理中...' : (mode === 'login' ? '登录' : '注册') }}
        </button>
        
        <p class="toggle-mode">
          {{ mode === 'login' ? '还没有账号？' : '已有账号？' }}
          <a href="#" @click.prevent="toggleMode">
            {{ mode === 'login' ? '立即注册' : '立即登录' }}
          </a>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.4rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #777;
  line-height: 1;
}

.close-button:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.error-message {
  background-color: #ffebee;
  color: #d32f2f;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
  font-size: 14px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  transition: border 0.2s;
}

.form-group input:focus {
  border-color: #4CAF50;
  outline: none;
}

.modal-footer {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  text-align: center;
}

.submit-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.2s;
}

.submit-button:hover {
  background-color: #45a049;
}

.submit-button:disabled {
  background-color: #9e9e9e;
  cursor: not-allowed;
}

.toggle-mode {
  margin-top: 15px;
  font-size: 14px;
  color: #666;
}

.toggle-mode a {
  color: #4CAF50;
  text-decoration: none;
  font-weight: 500;
}

.toggle-mode a:hover {
  text-decoration: underline;
}
</style>
