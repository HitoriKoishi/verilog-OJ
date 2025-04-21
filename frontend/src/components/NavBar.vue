<script setup>
import { useRouter } from 'vue-router';
import { ref, computed, inject } from 'vue';
import LoginModal from './LoginModal.vue';
import axios from 'axios'; // 引入axios用于发送HTTP请求

const router = useRouter();

const navItems = [
    { name: '首页', path: '/' },
    { name: '题目列表', path: '/problem/all' },
    { name: '学习路径', path: '/learning-path' },
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

const handleLogout = async () => {
    try {
        // 调用后端登出API
        const response = await axios.post('/api/user/logout');

        if (response.data.status === 'success') {
            // 后端注销成功后，执行前端登出逻辑
            logout();
            router.push('/');
        }
    } catch (error) {
        console.error('登出失败:', error);
        // 即使请求失败，也尝试在前端执行登出
        logout();
        router.push('/');
    }
};
</script>

<template>
    <div>
        <nav class="navbar">
            <div class="navbar-brand">Veri-OJ</div>
            <div class="navbar-menu">
                <div v-for="item in navItems" :key="item.name" class="navbar-item"
                    :class="{ 'active': currentRoute === item.path }" @click="navigateTo(item.path)">
                    {{ item.name }}
                </div>
                <div v-if="isLoggedIn && currentUser?.is_admin" class="navbar-item"
                    :class="{ 'active': currentRoute === '/admin' }" @click="navigateTo('/admin')">
                    管理员面板
                </div>
            </div>

            <div class="auth-container">
                <template v-if="isLoggedIn">
                    <div class="user-info">
                        <span>{{ currentUser.username }}</span>
                        <div class="dropdown-menu">
                            <div class="dropdown-item" @click="navigateTo('/user/profile')">个人中心</div>
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
    background-color: var(--navbar-bg);
    color: var(--navbar-text);
    padding: 0 var(--spacing-lg);
    height: 60px;
    justify-content: space-between;
}

.navbar-brand {
    font-size: 1.5rem;
    font-weight: bold;
    margin-right: var(--spacing-xl);
    color: var(--navbar-text);
}

.navbar-menu {
    display: flex;
    gap: var(--spacing-lg);
    flex-grow: 1;
}

.navbar-item {
    cursor: pointer;
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--radius-sm);
    transition: all var(--transition-normal);
    position: relative;
    color: var(--navbar-text);
}

.navbar-item:hover {
    background-color: var(--navbar-hover);
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
}

.navbar-item.active {
    background-color: var(--navbar-active);
    font-weight: bold;
}

.navbar-item.active:hover {
    background-color: var(--navbar-active);
}

.navbar-item::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    width: 0;
    height: 2px;
    background-color: var(--navbar-text);
    transition: all var(--transition-normal);
    transform: translateX(-50%);
}

.navbar-item:hover::after {
    width: 80%;
}

/* 认证相关样式 */
.auth-container {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    margin-left: auto;
}

.auth-button {
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--radius-sm);
    cursor: pointer;
    border: none;
    font-size: 0.875rem;
    transition: all var(--transition-fast);
}

.login {
    background-color: transparent;
    color: var(--navbar-text);
    border: 1px solid var(--navbar-text);
}

.login:hover {
    background-color: var(--navbar-hover);
}

.register {
    background-color: var(--navbar-active);
    color: var(--navbar-text);
}

.register:hover {
    background-color: var(--navbar-hover);
}

/* 用户信息样式 */
.user-info {
    position: relative;
    padding: var(--spacing-xs) var(--spacing-sm);
    cursor: pointer;
    border-radius: var(--radius-sm);
    transition: background-color var(--transition-fast);
    color: var(--navbar-text);
}

.user-info:hover {
    background-color: var(--navbar-hover);
}

.dropdown-menu {
    position: absolute;
    top: 100%;
    right: 0;
    background-color: var(--background-color);
    border-radius: var(--radius-sm);
    box-shadow: var(--shadow-md);
    width: 120px;
    display: none;
    z-index: var(--z-dropdown);
    border: 1px solid var(--border-color);
}

.user-info:hover .dropdown-menu {
    display: block;
}

.dropdown-item {
    padding: var(--spacing-sm) var(--spacing-md);
    color: var(--text-primary);
    transition: background-color var(--transition-fast);
}

.dropdown-item:hover {
    background-color: var(--surface-color);
}

/* 响应式设计 */
@media (max-width: 768px) {
    .navbar {
        font-size: 0.75rem;
        padding: 0 var(--spacing-md);
    }
    
    .navbar-brand {
        font-size: 0.8rem;
        margin-right: var(--spacing-md);
    }

    .navbar-menu {
        font-size: 0.75rem;
        gap: var(--spacing-sm);
    }
}
</style>
