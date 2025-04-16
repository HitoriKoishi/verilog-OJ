<script setup>
// 首页组件逻辑
</script>

<template>
  <div class="home container">
    <h1 class="title text-primary">欢迎使用 Veri-OJ</h1>
    <p class="description text-secondary">这是一个用于 Verilog 编程练习和学习的在线评测系统。</p>
    
    <div class="features flex gap-md">
      <div class="feature card">
        <h2 class="feature-title text-primary">学习 Verilog</h2>
        <p class="feature-description text-secondary">提供丰富的 Verilog 编程题目和学习资源</p>
      </div>
      
      <div class="feature card">
        <h2 class="feature-title text-primary">在线评测</h2>
        <p class="feature-description text-secondary">即时代码提交与自动评测反馈</p>
      </div>
      
      <div class="feature card">
        <h2 class="feature-title text-primary">跟踪进度</h2>
        <p class="feature-description text-secondary">记录学习历程，查看解题统计</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  /* min-height: calc(100vh - var(--spacing-xl) * 2); */
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  font-size: 2.5rem;
  margin-bottom: var(--spacing-lg);
  text-align: center;
  font-weight: bold;
}

.description {
  font-size: 1.2rem;
  margin-bottom: var(--spacing-xl);
  text-align: center;
}

.features {
  width: 100%;
  justify-content: space-between;
  flex-wrap: wrap;
}

.feature {
  flex: 1;
  min-width: 300px;
  margin: var(--spacing-sm);
  transition: transform var(--transition-normal);
}

.feature:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.feature-title {
  font-size: 1.5rem;
  margin-bottom: var(--spacing-md);
  font-weight: 600;
}

.feature-description {
  line-height: 1.6;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .features {
    flex-direction: column;
  }

  .feature {
    margin: var(--spacing-sm) 0;
  }

  .title {
    font-size: 2rem;
  }

  .description {
    font-size: 1.1rem;
  }
}
</style>
