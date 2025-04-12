<script setup>
import { ref, onMounted } from 'vue';

// 模拟用户数据
const userData = ref({
  username: 'user123',
  email: 'user@example.com'
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

// 获取用户数据
onMounted(() => {
  // 实际应用中，这里会从API获取用户数据
  userData.value.username = 'user123';
  userData.value.email = 'user@example.com';
});

// 修改用户名 - 更新逻辑，移除密码验证
const updateUsername = async () => {
  // 表单验证
  if (!usernameForm.value.newUsername) {
    message.value = '请填写新用户名';
    messageType.value = 'error';
    return;
  }

  usernameSubmitting.value = true;
  
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 更新本地数据
    userData.value.username = usernameForm.value.newUsername;
    usernameForm.value.newUsername = '';
    
    message.value = '用户名修改成功';
    messageType.value = 'success';
  } catch (error) {
    message.value = '修改失败，请稍后重试';
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
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 清空表单
    passwordForm.value.currentPassword = '';
    passwordForm.value.newPassword = '';
    passwordForm.value.confirmPassword = '';
    
    message.value = '密码修改成功';
    messageType.value = 'success';
  } catch (error) {
    message.value = '修改失败，请稍后重试';
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
      
      <!-- 修改用户名 - 移除密码输入框 -->
      <div class="account-section">
        <h2>修改用户名</h2>
        <form @submit.prevent="updateUsername">
          <div class="form-group">
            <label for="newUsername">新用户名</label>
            <input 
              id="newUsername" 
              v-model="usernameForm.newUsername" 
              type="text" 
              placeholder="输入新用户名"
              required
            />
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
            <input 
              id="currentPassword" 
              v-model="passwordForm.currentPassword" 
              type="password" 
              placeholder="输入当前密码"
              required
            />
          </div>
          
          <div class="form-group">
            <label for="newPassword">新密码</label>
            <input 
              id="newPassword" 
              v-model="passwordForm.newPassword" 
              type="password" 
              placeholder="输入新密码"
              required
            />
          </div>
          
          <div class="form-group">
            <label for="confirmPassword">确认新密码</label>
            <input 
              id="confirmPassword" 
              v-model="passwordForm.confirmPassword" 
              type="password" 
              placeholder="再次输入新密码"
              required
            />
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

.user-info, .account-section {
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
