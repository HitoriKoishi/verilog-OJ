# Verilog 在线评测系统

这是一个基于 Vue 3 + Vite 的 Verilog 在线评测系统前端项目。系统允许用户提交 Verilog 代码并自动评测结果。

## 环境要求

### 前端环境
- Node.js >= 14.0.0
- npm >= 6.0.0 或 yarn >= 1.22.0
- Vue 3
- Vite

### 后端环境
- Python >= 3.8
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-CORS
- 适用于 Verilog 仿真的环境：
  - Icarus Verilog (iverilog) 或其他 Verilog 编译器
  - GTKWave (可选，用于查看波形)

## 安装与运行

### 前端

```bash
# 进入前端项目目录
cd frontend

# 安装依赖
npm install
# 或
yarn install

# 运行开发服务器
npm run dev
# 或
yarn dev

# 构建生产版本
npm run build
# 或
yarn build
```

### 后端

```bash
# 进入后端项目目录
cd backend

# 创建并激活虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行服务器
python app.py
```

## 主要功能

- 用户注册与登录
- 浏览题目列表
- 查看题目详情
- 在线编写与提交 Verilog 代码
- 自动保存代码草稿
- 查看历史提交记录
- 实时评测结果反馈

---

原始模板信息:

# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).
