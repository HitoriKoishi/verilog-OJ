<script setup>
import Footer from './components/Footer.vue';
import NavBar from './components/NavBar.vue';
import { ref, onMounted, provide } from 'vue';

const isLoading = ref(true);
const hasError = ref(false);
const errorMessage = ref('');

// 用户登录状态管理
const isLoggedIn = ref(false);
const currentUser = ref(null);

const login = (user) => {
  isLoggedIn.value = true;
  currentUser.value = user;
  localStorage.setItem('user', JSON.stringify(user));
};

const logout = () => {
  isLoggedIn.value = false;
  currentUser.value = null;
  localStorage.removeItem('user');
};

// 提供登录状态和方法给子组件
provide('auth', {
  isLoggedIn,
  currentUser,
  login,
  logout
});

onMounted(() => {
  // 模拟页面加载完成
  setTimeout(() => {
    isLoading.value = false;
  }, 500);
  
  // 添加全局错误处理
  window.addEventListener('error', (event) => {
    hasError.value = true;
    errorMessage.value = event.message || '页面加载出错';
    console.error('页面错误:', event);
  });

  // 检查本地存储中的用户信息
  const savedUser = localStorage.getItem('user');
  if (savedUser) {
    try {
      currentUser.value = JSON.parse(savedUser);
      isLoggedIn.value = true;
    } catch (e) {
      console.error('无法解析存储的用户信息', e);
    }
  }
});
</script>

<template>
  <div class="app">
    <NavBar />
    <main class="main-content">
      <!-- 加载状态 -->
      <div v-if="isLoading" class="loading-container flex flex-col items-center">
        <div class="loading-spinner"></div>
        <p class="text-secondary">页面加载中...</p>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="hasError" class="error-container card">
        <h2 class="text-primary">加载出错</h2>
        <p class="text-secondary">{{ errorMessage }}</p>
        <button class="button" @click="window.location.reload()">重新加载</button>
      </div>

      <!-- 正常内容（包含过渡） -->
      <div v-else class="content-wrapper">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component 
              :is="Component" 
              class="route-content"
              :key="$route.path" />
          </transition>
        </router-view>
      </div>
    </main>
    <Footer />
  </div>
</template>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-family-base);
  line-height: 1.6;
  color: var(--text-primary);
  background-color: var(--surface-color);
  overflow-x: hidden;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--surface-color);
  overflow-x: hidden; /* 防止水平滚动 */
}

.main-content {
  flex: 1;
  position: relative;
  /* display: flex; */
  flex-direction: column;
  padding: var(--spacing-lg);
  min-height: 100px;
  width: 90%;
  max-width: var(--container-xl);
  margin: 0 auto;
}

.content-wrapper {
  position: relative;
  min-height: 400px;
}

.loading-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: var(--z-fixed);
  gap: var(--spacing-md);
}

.loading-spinner {
  border: 4px solid var(--border-color);
  border-radius: 50%;
  border-top: 4px solid var(--primary-color);
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  text-align: center;
  max-width: 500px;
  margin: 0 auto;
}

h1, h2, h3 {
  margin-bottom: var(--spacing-md);
}

a {
  text-decoration: none;
  color: var(--primary-color);
  transition: color var(--transition-fast);
}

a:hover {
  color: var(--primary-hover);
}

/* 响应式布局 */
@media screen and (max-width: 1200px) {
  .main-content {
    width: 95%;
    padding: var(--spacing-md);
  }
}

@media screen and (max-width: 768px) {
  .main-content {
    width: 100%;
    padding: var(--spacing-sm);
  }
}

/* 路由过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: 
    opacity var(--transition-normal),
    transform var(--transition-normal);
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(var(--spacing-sm));
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(calc(var(--spacing-sm) * -1));
}

.route-content {
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  margin: 0 auto;
  max-width: var(--container-xl);
}
</style>
