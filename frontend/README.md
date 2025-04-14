# Verilog 在线评测系统

这是一个基于 Vue 3 + Vite 的 Verilog 在线评测系统前端项目。系统允许用户提交 Verilog 代码并自动评测结果。

## [返回](../README.md)

## 环境要求

- Node.js >= 14.0.0
- npm >= 6.0.0 或 yarn >= 1.22.0
- Vue 3
- Vite

## 安装与运行

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

## 主要功能

- 用户注册与登录
- 浏览题目列表
- 查看题目详情
- 在线编写与提交 Verilog 代码
- 自动保存代码草稿
- 查看历史提交记录
- 实时评测结果反馈

项目结构

```
frontend/
├── public/            # 静态资源
├── src/
│   ├── api/           # API 请求接口
│   ├── assets/        # 项目资源文件
│   ├── components/    # 通用组件
│   │   ├── NavBar.vue         # 导航栏组件
│   │   └── LoginModal.vue     # 登录模态框
│   ├── views/         # 页面视图
│   │   ├── Home.vue           # 首页
│   │   ├── ProblemSubmit.vue  # 题目提交页面
│   │   ├── ProblemList.vue    # 题目列表界面
│   │   └── UserProfile.vue    # 个人信息界面
│   ├── App.vue        # 根组件
│   └── main.js        # 入口文件
└── index.html         # 入口界面
```

API 接口
前端通过 Axios 与后端 API 进行交互，主要接口包括：

用户相关：登录、注册、登出、检查登录状态
题目相关：获取题目列表、获取题目详情
代码相关：保存草稿、加载草稿、提交代码
提交相关：获取提交结果、获取波形文件
