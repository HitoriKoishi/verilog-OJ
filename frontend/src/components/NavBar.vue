<script setup>
import { useRouter } from 'vue-router';
import { ref, computed, inject } from 'vue';
import LoginModal from './LoginModal.vue';

const router = useRouter();

const navItems = [
    { name: '首页', path: '/' },
    { name: '题目列表', path: '/problems' },
    { name: '关于我们', path: '/about' },
];

const navigateTo = (path) => {
    router.push(path);
};

// 计算当前活动路由
const currentRoute = computed(() => router.currentRoute.value.path);

// 引入身份验证状态
const { isLoggedIn, currentUser, logout } = inject('auth');

// 控制登录模态窗口
const showLoginModal = ref(false);
const isRegistering = ref(false);

const openLoginModal = (isRegister = false) => {
    isRegistering.value = isRegister;
    showLoginModal.value = true;
};

const closeLoginModal = () => {
    showLoginModal.value = false;
};

const handleLogout = () => {
    logout();
    router.push('/');
};
</script>

<template>
    <div>
        <nav class="navbar">
            <div class="navbar-brand">Verilog OJ</div>
            <div class="navbar-menu">
                <div v-for="item in navItems" :key="item.name" class="navbar-item"
                    :class="{ 'active': currentRoute === item.path }" @click="navigateTo(item.path)">
                    {{ item.name }}
                </div>
            </div>

            <div class="auth-container">
                <template v-if="isLoggedIn">
                    <div class="user-info">
                        <span>{{ currentUser.username }}</span>
                        <div class="dropdown-menu">
                            <div class="dropdown-item" @click="navigateTo('/profile')">个人中心</div>
                            <div class="dropdown-item" @click="handleLogout">退出登录</div>
                        </div>
                    </div>
                </template>
                <template v-else>
                    <button class="auth-button login" @click="openLoginModal(false)">登录</button>
                    <button class="auth-button register" @click="openLoginModal(true)">注册</button>
                </template>
            </div>
        </nav>

        <!-- 登录/注册模态窗口 -->
        <LoginModal v-if="showLoginModal" :isRegistering="isRegistering" @close="closeLoginModal" />
    </div>
</template>

<style scoped>
.navbar {
    display: flex;
    align-items: center;
    background-color: #333;
    color: white;
    padding: 0 20px;
    height: 60px;
    justify-content: space-between;
}

.navbar-brand {
    font-size: 1.5rem;
    font-weight: bold;
    margin-right: 30px;
}

.navbar-menu {
    display: flex;
    gap: 20px;
    flex-grow: 1;
}

.navbar-item {
    cursor: pointer;
    padding: 5px 10px;
    border-radius: 4px;
    transition: all 0.3s ease;
    position: relative;
}

.navbar-item:hover {
    background-color: #444;
    transform: translateY(-2px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.navbar-item.active {
    background-color: #4CAF50;
    font-weight: bold;
}

.navbar-item.active:hover {
    background-color: #45a049;
}

.navbar-item::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    width: 0;
    height: 2px;
    background-color: #4CAF50;
    transition: all 0.3s ease;
    transform: translateX(-50%);
}

.navbar-item:hover::after {
    width: 80%;
}

/* 认证相关样式 */
.auth-container {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-left: auto;
}

.auth-button {
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
    border: none;
    font-size: 14px;
    transition: all 0.2s ease;
}

.login {
    background-color: transparent;
    color: white;
    border: 1px solid white;
}

.login:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.register {
    background-color: #4CAF50;
    color: white;
}

.register:hover {
    background-color: #45a049;
}

/* 用户信息样式 */
.user-info {
    position: relative;
    padding: 6px 12px;
    cursor: pointer;
    border-radius: 4px;
}

.user-info:hover {
    background-color: #444;
}

.dropdown-menu {
    position: absolute;
    top: 100%;
    right: 0;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    width: 120px;
    display: none;
    z-index: 1000;
}

.user-info:hover .dropdown-menu {
    display: block;
}

.dropdown-item {
    padding: 10px 15px;
    color: #333;
    transition: background-color 0.2s;
}

.dropdown-item:hover {
    background-color: #f5f5f5;
}
</style>
