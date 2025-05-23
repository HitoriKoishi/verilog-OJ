from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from enum import IntEnum
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db
from pathlib import Path
from functools import wraps
from flask import request, jsonify
from flask_login import current_user

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent
PROB_DIR = BASE_DIR/"Prob"
IVERILOG = BASE_DIR/"iverilog"/"bin"/"iverilog.exe"
VVP = BASE_DIR/"iverilog"/"bin"/"vvp.exe"


class ErrorCode(IntEnum):
    SUCCESS             = 0
    ERROR_COMPILE_FAIL  = 1
    ERROR_SIM_LOAD_FAIL = 2
    ERROR_SIM_RUN_FAIL  = 3
    ERROR_SIM_TIMEOUT   = 4
    ERROR_MISMATCH      = 5
    ERROR_BAT_NOT_FOUND = 6
    ERROR_UNKNOWN       = 7

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)                        # 用户ID
    username = db.Column(db.String(80), unique=True, nullable=False)    # 用户名
    email = db.Column(db.String(120), unique=True, nullable=True)       # 新增邮箱字段
    password_hash = db.Column(db.String(128), nullable=False)           # 密码哈希值
    is_admin = db.Column(db.Boolean, default=False)  # 新增管理员字段
    def get_id(self):
        return str(self.id)               
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f'<User {self.username}>'

class UserCode(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)         # 用户ID
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'), primary_key=True)   # ProbID
    draft_code = db.Column(db.Text)                                                     # 暂存代码
    updated_at = db.Column(db.DateTime)                                                 # 暂存时间

class SubmissionStatus():
    QUEUED = 'queued'
    RUNNING = 'running'
    SUCCESS = 'success'
    FAILED = 'failed'

class SimulationResult:
    def __init__(self):
        self.error_code = ErrorCode.ERROR_UNKNOWN
        self.log_path = ""
        self.waveform_path = ""


class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)            # 题目ID
    folder_path = db.Column(db.String(200), nullable=False) # 题目文件夹路径（相对于PROB_DIR）
    title = db.Column(db.String(100))                       # 标题
    description = db.Column(db.Text)                        # 题目描述
    code_temp = db.Column(db.Text)                         # 代码模板
    difficulty = db.Column(db.String(20), default='简单')   # 难度
    tags = db.Column(db.String(200))                       # 标签
    pre_problems = db.Column(db.String(200))              # 前置题目ID列表，用逗号分隔
    next_problems = db.Column(db.String(200))              # 后置题目ID列表，用逗号分隔

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)# 32位短submitID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))       # 用户ID
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id')) # ProbID
    code = db.Column(db.Text)                                       # 提交代码
    status = db.Column(db.String(20), default=SubmissionStatus.QUEUED)             # 添加默认状态
    error_code = db.Column(db.String(20), nullable=True)            # 错误码（与ErrorCode对应）
    log_path = db.Column(db.String(200), nullable=True)             # 限制路径长度
    waveform_path = db.Column(db.String(200), nullable=True)        # 限制路径长度
    created_at = db.Column(db.DateTime, default=datetime.now())     # 添加默认时间


def login_required(func):
    """自定义 login_required 装饰器，检查用户是否已登录"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({"error": "用户未登录"}), 401
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({"error": "需要管理员权限"}), 403
        return func(*args, **kwargs)
    return decorated_function