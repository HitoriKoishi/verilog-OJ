<script setup>
import { useRouter } from 'vue-router';
import { problemState } from '../store/problemState';

const router = useRouter();

const navigateToProblems = (tag) => {
  problemState.setSelectedTags([tag]);
  router.push('/problem/all');
};
</script>

<template>
  <div class="home container">
    <h1 class="title text-primary">欢迎使用 Veri-OJ</h1>
    <p class="description text-secondary">这是一个用于 Verilog 编程练习和学习的在线评测系统。</p>
    
    <!-- 学习路径卡片 -->
    <div class="learning-paths grid grid-cols-3 gap-lg mb-xl">
      <!-- Verilog语法卡片 -->
      <div class="card card-hover" @click="navigateToProblems('Verilog语法')" role="button">
        <div class="card-body">
          <h3 class="card-title">Verilog语法</h3>
          <div class="icon-container mb-md">
            <svg viewBox="0 0 100 100" class="icon">
              <!-- 代码符号图标 -->
              <path d="M30,20 L10,50 L30,80" 
                    fill="none" 
                    stroke="currentColor" 
                    stroke-width="8" 
                    stroke-linecap="round"/>
              <path d="M70,20 L90,50 L70,80" 
                    fill="none" 
                    stroke="currentColor" 
                    stroke-width="8" 
                    stroke-linecap="round"/>
              <path d="M45,15 L55,85" 
                    fill="none" 
                    stroke="currentColor" 
                    stroke-width="8" 
                    stroke-linecap="round"/>
            </svg>
          </div>
          <ul class="feature-list">
            <li>掌握 Verilog HDL 基础语法</li>
            <li>理解模块化设计思想</li>
            <li>学习常用语言结构</li>
          </ul>
        </div>
      </div>

      <!-- 组合逻辑卡片 -->
      <div class="card card-hover" @click="navigateToProblems('组合逻辑')" role="button">
        <div class="card-body">
          <h3 class="card-title">组合逻辑</h3>
          <div class="icon-container mb-md">
            <svg viewBox="0 0 100 100" class="icon">
              <!-- 与门图标 -->
              <path d="M20,20 L20,80 Q20,80 40,80 Q70,80 80,50 Q70,20 40,20 Q20,20 20,20 Z" 
                    fill="none" 
                    stroke="currentColor" 
                    stroke-width="4"/>
              <line x1="10" y1="30" x2="20" y2="30" 
                    stroke="currentColor" 
                    stroke-width="4"/>
              <line x1="10" y1="70" x2="20" y2="70" 
                    stroke="currentColor" 
                    stroke-width="4"/>
              <line x1="80" y1="50" x2="90" y2="50" 
                    stroke="currentColor" 
                    stroke-width="4"/>
            </svg>
          </div>
          <ul class="feature-list">
            <li>学习基本逻辑门电路</li>
            <li>设计组合逻辑电路</li>
            <li>实现功能性数字系统</li>
          </ul>
        </div>
      </div>

      <!-- 时序逻辑卡片 -->
      <div class="card card-hover" @click="navigateToProblems('时序逻辑')" role="button">
        <div class="card-body">
          <h3 class="card-title">时序逻辑</h3>
          <div class="icon-container mb-md">
            <svg viewBox="0 0 100 100" class="icon">
              <!-- 时钟波形图标 -->
              <path d="M10,50 L30,50 L30,20 L50,20 L50,50 L70,50 L70,20 L90,20" 
                    fill="none" 
                    stroke="currentColor" 
                    stroke-width="4" 
                    stroke-linejoin="round"/>
              <!-- 时钟边框 -->
              <circle cx="50" cy="50" r="40" 
                      fill="none" 
                      stroke="currentColor" 
                      stroke-width="2" 
                      stroke-dasharray="4 4"/>
            </svg>
          </div>
          <ul class="feature-list">
            <li>理解时序逻辑基本概念</li>
            <li>掌握触发器和寄存器</li>
            <li>设计状态机和控制系统</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 原有的功能卡片 -->
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
  padding: var(--spacing-xl) 0;
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

/* 学习路径卡片样式 */
.icon-container {
  width: 100%;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-color);
}

.icon {
  width: 80px;
  height: 80px;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li {
  color: var(--text-secondary);
  margin-bottom: var(--spacing-sm);
  position: relative;
  padding-left: var(--spacing-lg);
}

.feature-list li::before {
  content: "•";
  color: var(--primary-color);
  position: absolute;
  left: 0;
  font-size: 1.5em;
  line-height: 1;
}

/* 原有功能卡片样式 */
.features {
  width: 100%;
  justify-content: space-between;
  flex-wrap: wrap;
}

.feature {
  flex: 1;
  min-width: 300px;
  margin: var(--spacing-sm);
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
  .learning-paths {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }

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

.card-hover {
  cursor: pointer;
}

.card-hover:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.card-hover:active {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}
</style>
