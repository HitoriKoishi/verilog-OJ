<script setup>
import { ref, inject, watch } from 'vue';
import { userApi } from '../api';

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

// 实际登录请求
const loginRequest = async () => {
    try {
        const response = await userApi.login(username.value,password.value);

        if (response.data.status === "success") {
            // 登录成功，更新认证状态
            login(response.data.user);
            return response.data.user;
        } else {
            throw new Error(response.error.message || '登录失败');
        }
    } catch (error) {
        throw new Error(error.response?.data?.message || error.message || '登录请求失败');
    }
};

// 实际注册请求
const registerRequest = async () => {
    try {
        const response = await userApi.register(
            username.value,
            password.value,
            email.value || null // 如果没有提供邮箱，则传null
        );

        if (response.data.status === "success") {
            // 注册成功后自动登录
            login(response.data.user);
            return response.data.user;
        } else {
            throw new Error(response.data.message || '注册失败');
        }
    } catch (error) {
        throw new Error(error.response?.data?.message || error.message || '注册请求失败');
    }
};

const handleSubmit = async () => {
    if (!validateForm()) return;

    isSubmitting.value = true;

    try {
        if (mode.value === 'login') {
            await loginRequest();
        } else {
            await registerRequest();
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
    // 只有当点击的是背景层本身才关闭模态框
    if (e.target === e.currentTarget) {
        closeModal();
    }
};
</script>

<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-content card" @click.stop>
      <div class="modal-header">
        <h2 class="text-primary">{{ mode === 'login' ? '用户登录' : '用户注册' }}</h2>
        <button class="close-button" @click="closeModal">&times;</button>
      </div>

      <form @submit.prevent="handleSubmit" class="modal-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model="username"
            type="text"
            class="input"
            required
            :placeholder="mode === 'register' ? '请设置用户名' : '请输入用户名'"
          />
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="password"
            type="password"
            class="input"
            required
            :placeholder="mode === 'register' ? '请设置密码' : '请输入密码'"
          />
        </div>

        <div v-if="mode === 'register'" class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            class="input"
            required
            placeholder="请再次输入密码"
          />
        </div>

        <div v-if="mode === 'register'" class="form-group">
          <label for="email">邮箱（选填）</label>
          <input
            id="email"
            v-model="email"
            type="email"
            class="input"
            placeholder="请输入邮箱"
          />
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div class="form-actions">
          <button type="submit" class="button" :disabled="isSubmitting">
            {{ isSubmitting ? '处理中...' : (mode === 'login' ? '登录' : '注册') }}
          </button>
          <button type="button" class="button button-secondary" @click="toggleMode">
            {{ mode === 'login' ? '还没有账号？立即注册' : '已有账号？立即登录' }}
          </button>
        </div>
      </form>
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
  align-items: center;
  justify-content: center;
  z-index: var(--z-modal);
}

.modal-content {
  width: 90%;
  max-width: 400px;
  margin: var(--spacing-md);
  background-color: var(--background-color);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-secondary);
  padding: var(--spacing-xs);
  transition: color var(--transition-fast);
}

.close-button:hover {
  color: var(--text-primary);
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.form-group label {
  color: var(--text-primary);
  font-weight: 500;
}

.button-secondary {
  background-color: var(--surface-color);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.button-secondary:hover {
  background-color: var(--border-color);
  transform: translateY(-1px);
}

.form-actions {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-md);
}

.error-message {
  color: var(--error-color);
  font-size: 0.875rem;
  padding: var(--spacing-xs);
  border-radius: var(--radius-sm);
  background-color: var(--surface-color);
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    padding: var(--spacing-md);
  }
}
</style>
