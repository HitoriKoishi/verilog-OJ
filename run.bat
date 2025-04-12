@echo off
echo 安装依赖...
pip install -r requirements.txt

echo 启动Verilog Online Judge服务...
set FLASK_APP=backend/app.py
set FLASK_ENV=backend/development
flask run

pause
