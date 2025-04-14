<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'
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
    const progressResponse = await axios.get(`${API_URL}/problem/status`, { withCredentials: true });
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
    if (completion_status === '已完成') return 'green';
    if (completion_status === '失败') return 'red';
    if (completion_status === '运行中') return 'yellow';
    return 'gray';
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

// 跳转题目
const goToProblem = (problemId) => {
  router.push(`/problem/${problemId}`)
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

            <!-- 统计信息 -->
            <div class="progress-section">
              <h2>进度</h2>
              <!-- 添加统计卡片 -->
              <div class="stats-container">
                <div class="stat-card">
                  <div class="stat-value">{{ progressStats.passed }}</div>
                  <div class="stat-label">已通过</div>
                </div>
                <div class="stat-card">
                  <div class="stat-value">{{ progressStats.submitted }}</div>
                  <div class="stat-label">已提交</div>
                </div>
                <div class="stat-card">
                  <div class="stat-value">{{ progressStats.total }}</div>
                  <div class="stat-label">总题数</div>
                </div>
              </div>
              <!-- 问题按钮 -->
              <div class="problem-buttons">
                <button
                  v-for="problem in progressData"
                  :key="problem.id"
                  :class="getButtonClass(problem.completion_status)"
                  @click="goToProblem(problem.id)"
                  :title="`查看题目 ${problem.id}`"
                >
                  {{ problem.id }}
                </button>
              </div>
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
  background-color: #56b85b;
  min-width: 60px;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  color: white;
}

/* 悬停效果 */
button:hover {
  background-color: #45a049;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

button:active {
    background-color: #56b85b;
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 禁用状态 */
button:disabled {
  background-color: #cccccc;
  opacity: 0.7;
  cursor: not-allowed;
  filter: grayscale(0.3);
}

.problem-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px; /* 添加按钮间距 */
}

/* 统计卡片样式 */
.stats-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #4caf50;
  margin-bottom: 8px;
}

/* 状态颜色优化 */
button.green {
  background: #4caf50;
}

button.red {
  background: #cf4334;
}

button.yellow {
  background: #f39c12;
}

button.gray {
  background: #95a5a6;
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

    .stats-container {
      grid-template-columns: 1fr;
    }
    
    .stat-card {
      padding: 15px;
    }
    
    .stat-value {
      font-size: 20px;
    }
}
</style>
