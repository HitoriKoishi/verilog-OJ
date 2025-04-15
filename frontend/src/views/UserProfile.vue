<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'
import { problemApi, userApi } from '../api';
import axios from 'axios'; // 添加axios导入
const router = useRouter();

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

// 刷题进度数据
const progressData = ref([]);
// 添加进度统计相关数据
const progressStats = ref({
  total: 0,
  passed: 0,
  submitted: 0
});

// 表单提交状态
const usernameSubmitting = ref(false);
const passwordSubmitting = ref(false);

// 提示消息
const message = ref('');
const messageType = ref('');

// 获取用户数据
onMounted(async () => {
    try {
        const response = await userApi.checkAuth();
        if (response.data.is_login) {
            // 获取到登录用户信息
            userData.value.username = response.data.user.username;

            // 如果需要获取更多用户信息（如邮箱），可以再发一个请求
            try {
                const userDetailsResponse = await userApi.getUserProfile();
                if (userDetailsResponse.data.email) {
                    userData.value.email = userDetailsResponse.data.email;
                }
            } catch (error) {
                // 获取用户详情失败，可能是API不存在，使用默认值
                userData.value.email = response.data.user.email || '未设置邮箱';
            }
            // 获取刷题进度
            await getProgressStatus();
        } else {
            // 未登录，重定向到登录页
            window.location.href = '/login';
        }
    } catch (error) {
        message.value = '获取用户信息失败，请重新登录';
        messageType.value = 'error';
    }
});


// 获取刷题进度
const getProgressStatus = async () => {
  try {
    const progressResponse = await problemApi.getProblemStatus({ withCredentials: true });
    progressData.value = progressResponse.data;
    
    // 计算统计信息
    progressStats.value = {
      total: progressData.value.length,
      passed: progressData.value.filter(p => p.completion_status === '已完成').length,
      submitted: progressData.value.filter(p => p.completion_status !== '未完成').length
    };
  } catch (error) {
    console.error('获取进度失败:', error);
  }
};

// 根据完成状态返回按钮的样式
function getButtonClass(completion_status) {
    if (completion_status === '已完成') return 'button-success';
    if (completion_status === '失败') return 'button-error';
    if (completion_status === '运行中') return 'button-warning';
    return 'button-disabled';
}

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
        const response = await userApi.newUsername({
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
        const response = await userApi.updatePassword({
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

// 跳转题目
const goToProblem = (problemId) => {
  router.push(`/problem/${problemId}`)
};
</script>

<template>
    <div class="user-profile container">
        <h1 class="text-primary">个人中心</h1>

        <div class="profile-container">
            <!-- 用户基本信息 -->
            <div class="user-info card">
                <h2 class="text-primary">账户信息</h2>
                <div class="info-item">
                    <span class="label text-secondary">用户名:</span>
                    <span class="value text-primary">{{ userData.username }}</span>
                </div>
                <div class="info-item">
                    <span class="label text-secondary">邮箱:</span>
                    <span class="value text-primary">{{ userData.email }}</span>
                </div>
            </div>

            <!-- 消息提示 -->
            <div v-if="message" :class="['message', messageType, 'card']">
                {{ message }}
            </div>

            <!-- 统计信息 -->
            <div class="progress-section card">
              <h2 class="text-primary">进度</h2>
              <!-- 统计卡片 -->
              <div class="stats-container">
                <div class="stat-card">
                  <div class="stat-value text-success">{{ progressStats.passed }}</div>
                  <div class="stat-label text-secondary">已通过</div>
                </div>
                <div class="stat-card">
                  <div class="stat-value text-info">{{ progressStats.submitted }}</div>
                  <div class="stat-label text-secondary">已提交</div>
                </div>
                <div class="stat-card">
                  <div class="stat-value text-primary">{{ progressStats.total }}</div>
                  <div class="stat-label text-secondary">总题数</div>
                </div>
              </div>
              <!-- 问题按钮列表 -->
              <div class="problem-buttons">
                <button
                  v-for="problem in progressData"
                  :key="problem.id"
                  :class="['button', getButtonClass(problem.completion_status)]"
                  @click="goToProblem(problem.id)"
                  :title="`查看题目 ${problem.id}`"
                >
                  {{ problem.id }}
                </button>
              </div>
            </div>

            <!-- 修改用户名 -->
            <div class="account-section card">
                <h2 class="text-primary">修改用户名</h2>
                <form @submit.prevent="updateUsername" class="form">
                    <div class="form-group">
                        <label for="newUsername" class="text-secondary">新用户名</label>
                        <input id="newUsername" 
                               v-model="usernameForm.newUsername" 
                               type="text" 
                               class="input"
                               placeholder="输入新用户名"
                               required />
                    </div>

                    <button type="submit" class="button" :disabled="usernameSubmitting">
                        {{ usernameSubmitting ? '提交中...' : '更新用户名' }}
                    </button>
                </form>
            </div>

            <!-- 修改密码 -->
            <div class="account-section card">
                <h2 class="text-primary">修改密码</h2>
                <form @submit.prevent="updatePassword" class="form">
                    <div class="form-group">
                        <label for="currentPassword" class="text-secondary">当前密码</label>
                        <input id="currentPassword" 
                               v-model="passwordForm.currentPassword" 
                               type="password"
                               class="input"
                               placeholder="输入当前密码" 
                               required />
                    </div>

                    <div class="form-group">
                        <label for="newPassword" class="text-secondary">新密码</label>
                        <input id="newPassword" 
                               v-model="passwordForm.newPassword" 
                               type="password"
                               class="input"
                               placeholder="输入新密码"
                               required />
                    </div>

                    <div class="form-group">
                        <label for="confirmPassword" class="text-secondary">确认新密码</label>
                        <input id="confirmPassword" 
                               v-model="passwordForm.confirmPassword" 
                               type="password"
                               class="input"
                               placeholder="再次输入新密码"
                               required />
                    </div>

                    <button type="submit" class="button" :disabled="passwordSubmitting">
                        {{ passwordSubmitting ? '提交中...' : '更新密码' }}
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.user-profile {
    padding: var(--spacing-lg);
}

h1 {
    margin-bottom: var(--spacing-xl);
    text-align: center;
}

.profile-container {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-lg);
}

.info-item {
    margin-bottom: var(--spacing-sm);
    display: flex;
}

.label {
    font-weight: 500;
    width: 100px;
}

.form {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
}

.button-success {
  background-color: var(--success-color);
}

.button-error {
  background-color: var(--error-color);
}

.button-warning {
  background-color: var(--warning-color);
}

.button-disabled {
  background-color: var(--text-disabled);
  cursor: not-allowed;
}

/* 统计卡片样式 */
.stats-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
  margin: var(--spacing-lg) 0;
}

.stat-card {
  background: var(--background-color);
  border-radius: var(--radius-sm);
  padding: var(--spacing-md);
  text-align: center;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: var(--spacing-xs);
}

.problem-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
  margin-top: var(--spacing-lg);
}

.problem-buttons button {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  transition: all var(--transition-fast);
}

.message {
    padding: var(--spacing-sm);
    border-radius: var(--radius-sm);
    margin-bottom: var(--spacing-md);
}

.message.success {
    background-color: color-mix(in srgb, var(--success-color) 10%, transparent);
    color: var(--success-color);
    border: 1px solid var(--success-color);
}

.message.error {
    background-color: color-mix(in srgb, var(--error-color) 10%, transparent);
    color: var(--error-color);
    border: 1px solid var(--error-color);
}

@media (max-width: 768px) {
    .user-profile {
        padding: var(--spacing-md);
    }

    .stats-container {
        grid-template-columns: 1fr;
    }
    
    .stat-card {
        padding: var(--spacing-sm);
    }
    
    .stat-value {
        font-size: 1.25rem;
    }
}
</style>
