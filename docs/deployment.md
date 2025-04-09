# Verilog Online Judge 部署指南

本文档介绍如何部署和运行 Verilog Online Judge 系统。

## 系统要求

- Docker 和 Docker Compose
- 4GB+ RAM
- 10GB+ 硬盘空间
- Linux/macOS/Windows 系统

## 基础部署

1. 克隆代码仓库：

```bash
git clone https://github.com/your-username/verilog-OJ.git
cd verilog-OJ
```

2. 创建环境变量文件：

```bash
# 创建 .env 文件
touch .env

# 填入以下内容
SECRET_KEY=your-secure-secret-key
DEBUG=False
```

3. 启动服务：

```bash
docker-compose up -d
```

4. 访问系统：

```
前端: http://localhost:8080
后端API: http://localhost:8000
管理界面: http://localhost:8000/admin
```

## 初始化数据

1. 创建超级管理员账户：

```bash
docker-compose exec backend python manage.py createsuperuser
```

2. 导入示例问题（可选）：

```bash
docker-compose exec backend python manage.py loaddata example_problems
```

## 生产环境部署

对于生产环境，建议：

1. 使用 Nginx 作为反向代理：

```bash
# 安装 Nginx
sudo apt-get install nginx

# 创建配置文件
sudo nano /etc/nginx/sites-available/verilog-oj

# 配置内容
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /admin {
        proxy_pass http://localhost:8000/admin;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 启用配置
sudo ln -s /etc/nginx/sites-available/verilog-oj /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

2. 启用 HTTPS：

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

3. 配置更安全的环境变量：

```bash
# 生成随机密钥
export SECRET_KEY=$(openssl rand -hex 32)

# 更新 .env 文件
echo "SECRET_KEY=$SECRET_KEY" > .env
echo "DEBUG=False" >> .env
```

## 自定义评测系统

Verilog评测系统位于 `backend/judge/judge_engine.py`，支持自定义评测逻辑：

1. 修改测试用例格式
2. 添加更多评测工具（如ModelSim等）
3. 自定义评分标准

示例：添加波形检查支持

```python
# 在_run_test_case方法中添加波形检查
def _verify_waveform(self, vcd_file, expected_pattern):
    # 实现波形检查逻辑
    pass
```

## 故障排除

1. 查看日志：

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f judge
```

2. 检查数据库：

```bash
docker-compose exec db psql -U postgres -d verilog_oj
```

3. 重启服务：

```bash
docker-compose restart
```

4. 完全重建：

```bash
docker-compose down
docker-compose up -d --build
```
