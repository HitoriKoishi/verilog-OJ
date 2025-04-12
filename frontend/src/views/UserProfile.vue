<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios'; // 添加axios导入

// 用户数据
const userData = ref({
    username: '',
    email: ''
});

// 修改用户名表单数据 
const usernameForm = ref({
    newUsername: ''
});

// 修改密码表单数据
const passwordForm = ref({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
});

// 表单提交状态
const usernameSubmitting = ref(false);
const passwordSubmitting = ref(false);

// 提示消息
const message = ref('');
const messageType = ref('');

// API基础URL
const API_URL = 'http://localhost:5000';

// 获取用户数据
onMounted(async () => {
    try {
        const response = await axios.get(`${API_URL}/user/check_auth`, { withCredentials: true });
        if (response.data.is_login) {
            // 获取到登录用户信息
            userData.value.username = response.data.user.username;

            // 如果需要获取更多用户信息（如邮箱），可以再发一个请求
            try {
                const userDetailsResponse = await axios.get(`${API_URL}/user/profile`, { withCredentials: true });
                if (userDetailsResponse.data.email) {
                    userData.value.email = userDetailsResponse.data.email;
                }
            } catch (error) {
                // 获取用户详情失败，可能是API不存在，使用默认值
                userData.value.email = response.data.user.email || '未设置邮箱';
            }
        } else {
            // 未登录，重定向到登录页
            window.location.href = '/login';
        }
    } catch (error) {
        message.value = '获取用户信息失败，请重新登录';
        messageType.value = 'error';
    }
});

// 修改用户名
const updateUsername = async () => {
    // 表单验证
    if (!usernameForm.value.newUsername) {
        message.value = '请填写新用户名';
        messageType.value = 'error';
        return;
    }

    usernameSubmitting.value = true;

    try {
        // 实际API调用
        const response = await axios.post(`${API_URL}/user/update_username`, {
            newUsername: usernameForm.value.newUsername
        }, { withCredentials: true });

        // 更新本地数据
        userData.value.username = usernameForm.value.newUsername;
        usernameForm.value.newUsername = '';

        message.value = '用户名修改成功';
        messageType.value = 'success';
    } catch (error) {
        message.value = error.response?.data?.error || '修改失败，请稍后重试';
        messageType.value = 'error';
    } finally {
        usernameSubmitting.value = false;
    }
};

// 修改密码
const updatePassword = async () => {
    // 表单验证
    if (!passwordForm.value.currentPassword || !passwordForm.value.newPassword || !passwordForm.value.confirmPassword) {
        message.value = '请填写所有必填字段';
        messageType.value = 'error';
        return;
    }

    if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
        message.value = '两次输入的新密码不一致';
        messageType.value = 'error';
        return;
    }

    passwordSubmitting.value = true;

    try {
        // 实际API调用
        const response = await axios.post(`${API_URL}/user/update_password`, {
            currentPassword: passwordForm.value.currentPassword,
            newPassword: passwordForm.value.newPassword
        }, { withCredentials: true });

        // 清空表单
        passwordForm.value.currentPassword = '';
        passwordForm.value.newPassword = '';
        passwordForm.value.confirmPassword = '';

        message.value = '密码修改成功';
        messageType.value = 'success';
    } catch (error) {
        message.value = error.response?.data?.error || '修改失败，请稍后重试';
        messageType.value = 'error';
    } finally {
        passwordSubmitting.value = false;
    }
};
</script>

<template>
    <div class="user-profile">
        <h1>个人中心</h1>

        <div class="profile-container">
            <!-- 用户基本信息 -->
            <div class="user-info">
                <h2>账户信息</h2>
                <div class="info-item">
                    <span class="label">用户名:</span>
                    <span class="value">{{ userData.username }}</span>
                </div>
                <div class="info-item">
                    <span class="label">邮箱:</span>
                    <span class="value">{{ userData.email }}</span>
                </div>
            </div>

            <!-- 消息提示 -->
            <div v-if="message" :class="['message', messageType]">
                {{ message }}
            </div>

            <!-- 修改用户名 -->
            <div class="account-section">
                <h2>修改用户名</h2>
                <form @submit.prevent="updateUsername">
                    <div class="form-group">
                        <label for="newUsername">新用户名</label>
                        <input id="newUsername" v-model="usernameForm.newUsername" type="text" placeholder="输入新用户名"
                            required />
                    </div>

                    <button type="submit" :disabled="usernameSubmitting">
                        {{ usernameSubmitting ? '提交中...' : '更新用户名' }}
                    </button>
                </form>
            </div>

            <!-- 修改密码 -->
            <div class="account-section">
                <h2>修改密码</h2>
                <form @submit.prevent="updatePassword">
                    <div class="form-group">
                        <label for="currentPassword">当前密码</label>
                        <input id="currentPassword" v-model="passwordForm.currentPassword" type="password"
                            placeholder="输入当前密码" required />
                    </div>

                    <div class="form-group">
                        <label for="newPassword">新密码</label>
                        <input id="newPassword" v-model="passwordForm.newPassword" type="password" placeholder="输入新密码"
                            required />
                    </div>

                    <div class="form-group">
                        <label for="confirmPassword">确认新密码</label>
                        <input id="confirmPassword" v-model="passwordForm.confirmPassword" type="password"
                            placeholder="再次输入新密码" required />
                    </div>

                    <button type="submit" :disabled="passwordSubmitting">
                        {{ passwordSubmitting ? '提交中...' : '更新密码' }}
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.user-profile {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
}

h1 {
    margin-bottom: 30px;
    text-align: center;
}

h2 {
    margin-bottom: 20px;
    color: #333;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
}

.profile-container {
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.user-info,
.account-section {
    background-color: #fff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.info-item {
    margin-bottom: 15px;
    display: flex;
}

.label {
    font-weight: bold;
    width: 100px;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
}

input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
}

button {
    background-color: #4caf50;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #45a049;
}

button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

.message {
    padding: 12px;
    border-radius: 4px;
    margin-bottom: 20px;
}

.success {
    background-color: #dff0d8;
    color: #3c763d;
    border: 1px solid #d6e9c6;
}

.error {
    background-color: #f2dede;
    color: #a94442;
    border: 1px solid #ebccd1;
}

@media (max-width: 768px) {
    .user-profile {
        padding: 10px;
    }

    .form-group {
        margin-bottom: 15px;
    }

    button {
        width: 100%;
    }
}
</style>
