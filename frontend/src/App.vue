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

const reloadPage = () => {
    window.location.reload();
};

</script>

<template>
    <div class="app">
        <NavBar />
        <main class="main-content">
            <!-- 加载状态 -->
            <div v-if="isLoading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>页面加载中...</p>
            </div>

            <!-- 错误状态 -->
            <div v-else-if="hasError" class="error-container">
                <h2>加载出错</h2>
                <p>{{ errorMessage }}</p>
                <button @click="reloadPage">重新加载</button>
            </div>

            <!-- 正常内容（包含过渡） -->
            <div v-else class="content-wrapper">
                <router-view v-slot="{ Component }">
                    <transition name="fade" mode="out-in">
                        <component :is="Component" class="route-content" :key="$route.path" />
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
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
    /* 添加背景色 */
    overflow-x: hidden;
    /* 防止整个页面出现水平滚动条 */
}

/* 修改主容器样式，确保内容不会溢出 */
.app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    overflow-x: hidden;
    /* 防止水平滚动 */
}

.main-content {
    flex: 1;
    position: relative;
    /* display: flex; */
    flex-direction: column;
    padding: 20px;
    min-height: 100px;
    max-width: 1400px;
    width: 90%;
    margin: 0 auto;
    overflow: hidden;
    /* 防止内容溢出 */
}

/* 添加布局稳定层 */
.content-wrapper {
    position: relative;
    min-height: 400px;
    /* 与加载容器高度保持一致 */
}

/* 优化加载容器 */
.loading-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 10;
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
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

/* 错误提示样式 */
.error-container {
    text-align: center;
    padding: 40px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
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

h1,
h2,
h3 {
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

a:active,
a:hover {
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

/* 新的过渡动画 */
.fade-enter-active,
.fade-leave-active {
    transition:
        opacity 0.3s ease,
        transform 0.3s ease;
}

.fade-enter-from {
    opacity: 0;
    transform: translateY(10px);
}

.fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

.route-content {
    padding: 20px;
    /* background: rgba(255, 255, 255, 0.486); */
    border-radius: 8px;
    /* box-shadow: 0 2px 12px rgba(0,0,0,0.08); */
    margin: 0 auto;
    max-width: 1000px;
}
</style>
