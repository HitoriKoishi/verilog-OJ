<template>
  <div class="about container">
    <h1 class="title text-primary">关于我们</h1>
    
    <div class="content">
      <section class="card mb-lg">
        <h2 class="section-title text-primary">项目介绍</h2>
        <p class="text-secondary">Veri-OJ 是一个专注于Verilog硬件描述语言学习和在线评测的平台。本项目旨在为数字电路与计算机组成原理课程的学习者提供一个实践平台，帮助学生更好地理解和掌握Verilog编程。</p>
      </section>

      <section class="card mb-lg">
        <h2 class="section-title text-primary">技术栈</h2>
        <div class="tech-stack">
          <div class="tech-item">
            <h3 class="text-primary">前端</h3>
            <ul class="text-secondary">
              <li>Vue 3 - 渐进式JavaScript框架</li>
              <li>Vite - 现代前端构建工具</li>
              <li>Vue Router - 路由管理</li>
              <li>CodeMirror - 代码编辑器</li>
              <li>WaveDrom - 波形显示</li>
            </ul>
          </div>
          <div class="tech-item">
            <h3 class="text-primary">后端</h3>
            <ul class="text-secondary">
              <li>Flask - Python Web框架</li>
              <li>SQLite - 轻量级数据库</li>
              <li>Icarus Verilog - 开源Verilog仿真工具</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="card mb-lg">
        <h2 class="section-title text-primary">项目开源</h2>
        <p class="text-secondary">本项目已在GitHub开源，欢迎访问我们的仓库：</p>
        <a href="https://github.com/HitoriKoishi/verilog-OJ" target="_blank" class="button button-primary mt-sm">
          访问 GitHub 仓库
        </a>
      </section>

      <section class="card mb-lg">
        <h2 class="section-title text-primary">快速开始</h2>
        <div class="setup-guide text-secondary">
          <h3>本地开发环境搭建</h3>
          <pre class="code-block">
# 克隆项目
git clone https://github.com/HitoriKoishi/verilog-OJ.git

# 前端设置
cd frontend
npm install
npm run dev

# 后端设置
cd backend
pip install -r requirements.txt
python app.py</pre>
        </div>
      </section>

      <section class="card">
        <h2 class="section-title text-primary">致谢</h2>
        <div class="text-secondary">
          <p>感谢所有为本项目做出贡献的开发者、测试者和使用者。</p>
          <p>感谢所有使用这个平台学习的同学们，你们的反馈是我们不断改进的动力。</p>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.about {
  padding: var(--spacing-lg) 0;
}

.title {
  font-size: 2rem;
  margin-bottom: var(--spacing-xl);
  text-align: center;
}

.content {
  max-width: 1000px;
  margin: 0 auto;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-xs);
  border-bottom: 2px solid var(--primary-color);
}

.mb-lg {
  margin-bottom: var(--spacing-lg);
}

.mt-sm {
  margin-top: var(--spacing-sm);
}

.tech-stack {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
}

.tech-item ul {
  list-style: none;
  padding: 0;
}

.tech-item li {
  margin: var(--spacing-xs) 0;
  padding-left: var(--spacing-md);
  position: relative;
}

.tech-item li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: var(--primary-color);
}

.code-block {
  background-color: var(--surface-color);
  padding: var(--spacing-md);
  border-radius: var(--radius-sm);
  overflow-x: auto;
  font-family: var(--font-family-mono);
  margin: var(--spacing-sm) 0;
  border: 1px solid var(--border-color);
}

.setup-guide h3 {
  margin-bottom: var(--spacing-sm);
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .about {
    padding: var(--spacing-md);
  }

  .content {
    width: 100%;
  }

  .tech-stack {
    grid-template-columns: 1fr;
  }
}
</style>