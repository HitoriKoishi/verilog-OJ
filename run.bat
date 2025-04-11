@echo off
echo 安装依赖...
pip install -r requirements.txt

echo 启动Verilog Online Judge服务...
set FLASK_APP=app.py
set FLASK_ENV=development
flask run

pause
