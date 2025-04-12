<script setup>
import NavBar from './components/NavBar.vue';
import { ref, onMounted, provide } from 'vue';

const isLoading = ref(true);
const hasError = ref(false);
const errorMessage = ref('');

const website = ref({ website_footer: '© 2025 在线判题系统' }); // 默认值，可根据需要更改
const version = ref('1.0.0'); // 默认版本号

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
      <div v-if="isLoading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>页面加载中...</p>
      </div>
      <div v-else-if="hasError" class="error-container">
        <h2>加载出错</h2>
        <p>{{ errorMessage }}</p>
        <button @click="window.location.reload()">重新加载</button>
      </div>
      <router-view v-else />
      <div class="footer">
        <p v-html="website.website_footer"></p>
        <p>Powered by <a href="https://github.com/HitoriKoishi/verilog-OJ">OnlineJudge</a>
          <span v-if="version">&nbsp; Version: {{ version }}</span>
        </p>
      </div>
    </main>
  </div>
</template>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f5f5f5; /* 添加背景色 */
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 20px;
  position: relative; /* 为加载指示器定位 */
}

/* 加载指示器样式 */
.loading-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 300px;
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #4CAF50;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 错误提示样式 */
.error-container {
  text-align: center;
  padding: 40px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  max-width: 500px;
  margin: 0 auto;
}

.error-container button {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 20px;
}

h1, h2, h3 {
  margin-bottom: 15px;
}

* {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}

a {
  text-decoration: none;
  background-color: transparent;
}

a:active, a:hover {
  outline-width: 0;
}

@media screen and (max-width: 1200px) {
  .content-app {
    margin-top: 160px;
    padding: 0 2%;
  }
}

@media screen and (min-width: 1200px) {
  .content-app {
    margin-top: 80px;
    padding: 0 2%;
  }
}

.footer {
  margin-top: 20px;
  margin-bottom: 10px;
  text-align: center;
  font-size: small;
}

.fadeInUp-enter-active {
  animation: fadeInUp .8s;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translate3d(0, 100%, 0);
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
}
</style>
