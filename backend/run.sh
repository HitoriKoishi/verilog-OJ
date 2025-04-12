#!/bin/bash

echo "安装依赖..."
pip install -r requirements.txt

echo "启动Verilog Online Judge服务..."
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
