# Verilog Online Judge

Verilog在线评测系统，支持Verilog代码的提交、评测和结果展示。

## 功能特点

- 用户管理：注册、登录、个人信息管理
- 题目管理：浏览题目、难度分级、分类标签
- 代码提交：在线编辑器、历史提交记录
- 评测系统：自动编译运行Verilog代码、结果比对
- 排行榜：按通过率、提交次数等维度排名

## 项目结构

```
verilog-OJ/
├── frontend/          # 前端代码 (Vue.js)
├── backend/           # 后端API和评测系统 (Django)
│   ├── api/           # API接口
│   ├── judge/         # 评测系统
│   ├── problems/      # 题目管理
│   └── users/         # 用户管理
├── docker/            # Docker配置文件
└── docs/              # 文档
```

## 部署和运行

请参考 [部署文档](./docs/deployment.md)

## 快速开始

```bash
# 使用Docker Compose启动所有服务
docker-compose up -d

# 访问系统
http://localhost:8080
```
