<script setup>
// 首页组件逻辑
</script>

<template>
  <div class="home">
    <h1>欢迎使用 Verilog OJ</h1>
    <p>这是一个用于 Verilog 编程练习和学习的在线评测系统。</p>
    <div class="features">
      <div class="feature">
        <h2>学习 Verilog</h2>
        <p>提供丰富的 Verilog 编程题目和学习资源</p>
      </div>
      <div class="feature">
        <h2>在线评测</h2>
        <p>即时代码提交与自动评测反馈</p>
      </div>
      <div class="feature">
        <h2>跟踪进度</h2>
        <p>记录学习历程，查看解题统计</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
  text-align: center;
}

.features {
  display: flex;
  justify-content: space-between;
  margin-top: 40px;
  flex-wrap: wrap;
}

.feature {
  flex: 1;
  min-width: 300px;
  margin: 15px;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .features {
    flex-direction: column;
  }
}
</style>
