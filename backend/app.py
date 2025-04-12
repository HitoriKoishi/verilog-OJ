from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
import json
from pathlib import Path
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from threading import Lock

simulation_lock = Lock()

# 导入 sim_run 模块
from run_sim import run_simulation as sim_run_verilog
from run_sim import ErrorCode
from run_sim import SimulationResult

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.secret_key = 'verilog-oj-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # 使用 SQLite 数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # 指定登录路由

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)            # id为exp文件夹后面的数字
    title = db.Column(db.String(100))                       # tile为exp/doc/doc.md的第一个一级标题
    description = db.Column(db.Text)                        # description为exp/doc/doc.md
    code_temp = db.Column(db.Text)                          # 代码模板
    difficulty = db.Column(db.String(20), default='简单')   # 难度字段
    tags = db.Column(db.String(200))                        # 标签字段

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)                        # 用户ID
    username = db.Column(db.String(80), unique=True, nullable=False)    # 用户名
    email = db.Column(db.String(120), unique=True, nullable=True)       # 新增邮箱字段
    password_hash = db.Column(db.String(128), nullable=False)           # 密码哈希值
    def get_id(self):
        return str(self.id)               
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserCode(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)         # 用户ID
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'), primary_key=True)   # ProbID
    draft_code = db.Column(db.Text)                                                     # 暂存代码
    updated_at = db.Column(db.DateTime)                                                 # 暂存时间

class Submission(db.Model):
    id = db.Column(db.String(6), primary_key=True)                  # 6位短submitID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))       # 用户ID
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id')) # ProbID
    code = db.Column(db.Text)                                       # 提交代码
    status = db.Column(db.String(20), default='queued')             # 添加默认状态
    error_code = db.Column(db.String(20))                           # 错误码（与ErrorCode对应）
    log_path = db.Column(db.String(200))                            # 限制路径长度
    waveform_path = db.Column(db.String(200))                       # 限制路径长度
    created_at = db.Column(db.DateTime, default=datetime.now())     # 添加默认时间

# ---------- 用户加载器 ----------
@login_manager.user_loader
def loadUser(user_id):
    return User.query.get(int(user_id))

# ---------- 登录路由 ----------
@app.route('/login', methods=['POST'])
def userLogin():
    username = request.get_json.get('username')
    password = request.get_json.get('password')
    if not username or not password:
        return jsonify({"status": "error", "msg": "需要用户名和密码"}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"status": "error", "msg": "用户名或密码错误"}), 401
    login_user(user)
    return jsonify({
        "status": "success",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    })

# ---------- 注销路由 ----------
@app.route('/logout', methods=['POST'])
@login_required
def logoutUser():
    logout_user()
    return jsonify({"status": "success"})

# ---------- 登录状态检查 ----------
@app.route('/check_auth', methods=['GET'])
def checkAuth():
    if current_user.is_authenticated:
        return jsonify({
            "is_login": True,
            "user": {
                "id": current_user.id,
                "username": current_user.username
            }
        })
    return jsonify({"is_login": False})

# ---------- 注册路由 ----------
@app.route('/register', methods=['POST'])
def registerUser():
    """注册接口，支持密码和邮箱"""
    username = request.get_json.get('username')
    password = request.get_json.get('password')
    email = request.get_json.get('email')
    # 验证存在性
    if not username or not password:
        return jsonify({"error": "用户名和密码为必填项"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "用户名已存在"}), 409
    if email and User.query.filter_by(email=email).first():
        return jsonify({"error": "邮箱已被注册"}), 409
    # 创建用户
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)    #自动登录
    return jsonify({
        "status": "success",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    })


# ---------- 保存代码草稿 ----------
@app.route('/problems/<int:id>', methods=['POST'])
@login_required
def saveDraft(id):
    """保存代码草稿"""
    user_id = current_user.id
    code = request.get_json.get('code')
    # 验证存在性
    if not (User.query.get(user_id)) or not (Problem.query.get(id)):
        return jsonify({"error": "用户或问题不存在"}), 404
    # 更新或创建暂存记录
    draft = UserCode.query.filter_by(
        user_id=user_id,
        problem_id=id
    ).first()
    if draft:
        draft.draft_code = code
        draft.updated_at = datetime.now()
    else:
        draft = UserCode(
            user_id=user_id,
            problem_id=id,
            draft_code=code,
            updated_at=datetime.now()
        )
        db.session.add(draft)
    db.session.commit()
    return jsonify({"status": "success"})


# ---------- 提交代码，创建提交ID ----------
@app.route('/problems/<int:id>/submit', methods=['POST'])
@login_required
def submitSolution(id):
    """提交代码"""
    user_id = current_user.id
    code = request.get_json.get('code')
    # 验证存在性
    if not (User.query.get(user_id)) or not (Problem.query.get(id)):
        return jsonify({"error": "用户或问题不存在"}), 404
    # 创建提交记录
    submission = Submission(
        id=str(uuid.uuid4()),
        user_id=user_id,
        problem_id=id,
        code=code,
        status='queued',  # 初始状态为排队中
        created_at=datetime.now()
    )
    db.session.add(submission)
    db.session.commit()
    return jsonify({"submission_id": submission.id})


# ---------- 获取提交结果，运行仿真 ----------
@app.route('/submissions/<submission_id>')
def getSubmission(submission_id):
    """触发仿真执行并返回结果"""
    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({"error": "提交记录不存在"}), 404
    # 最终状态直接返回
    if submission.status in ['success', 'failed']:
        return _format_response(submission)
    # 加锁防止并发执行
    with simulation_lock:
        # 刷新对象状态
        submission = Submission.query.get(submission_id)
        if submission.status != 'queued':
            return _format_response(submission)
        try:
            # 更新为运行状态
            submission.status = 'running'
            db.session.commit()
            # 执行仿真
            sim_result = sim_run_verilog(
                expnum=submission.problem_id,
                submission_id=submission_id
            )
            # 更新数据库记录
            submission.status = 'success' if sim_result.error_code == ErrorCode.SUCCESS else 'failed'
            submission.error_code = sim_result.error_code.name
            submission.log_path = sim_result.log_path
            submission.waveform_path = sim_result.waveform_path
        except Exception as e:
            # 错误处理
            submission.status = 'failed'
            submission.error_code = str(e)
            submission.log_path = ""
            submission.waveform_path = ""
            app.logger.error(f"Submission {submission_id} failed: {str(e)}", exc_info=True)
        finally:
            db.session.commit()
    return _format_response(submission)


def _format_response(submission):
    """统一响应格式化"""
    response_data = {
        "problem_id": submission.problem_id,
        "status": submission.status,
        "error_code": submission.error_code,
        "log_path": submission.log_path,
        "waveform_path": submission.waveform_path,
        "created_at": submission.created_at.isoformat()
    }
    return jsonify(response_data)


# ---------- 更新Prob数据库 ----------
def updateProblems():
    """根据exp文件夹更新数据库"""
    # 获取现有问题映射 {id: problem_obj}
    existing_problems = {p.id: p for p in Problem.query.all()}
    current_ids = set()
    # 扫描 exp 开头的文件夹
    for exp_dir in BASE_DIR.glob("exp*"):
        if not exp_dir.is_dir():
            continue
        # 提取实验 ID
        try:
            exp_id = int(exp_dir.name[3:])  # 从 "exp1" 提取 1
        except ValueError:
            continue  # 跳过非法格式的文件夹
        # 读取文档文件
        current_ids.add(exp_id)
        default_difficulty = '简单'
        default_tags = '默认TAG'
        doc_dir = exp_dir / "doc"
        doc_path = doc_dir / "doc.md"
        temp_code_path = doc_dir / "temp_module.v"
        try:
            with open(doc_path, "r", encoding="utf-8") as f:
                doc_content = f.read()
            # 提取第一个一级标题
            title = next(
                    line.strip("# \n") for line in doc_content.splitlines() 
                    if line.startswith("# ")
            )
            # 读取代码模板（允许为空）
            code_temp = ""
            if temp_code_path.exists():
                with open(temp_code_path, "r", encoding="utf-8") as f:
                    code_temp = f.read()
            # 更新或创建记录
            if exp_id in existing_problems:
                # 保留原有难度和标签
                problem = existing_problems[exp_id]
                problem.title = title
                problem.description = doc_content
                problem.code_temp = code_temp
            else:
                # 新增记录使用默认值
                problem = Problem(
                    id=exp_id,
                    title=title,
                    description=doc_content,
                    code_temp=code_temp,
                    difficulty=default_difficulty,
                    tags=default_tags
                )
                db.session.add(problem)
        except (FileNotFoundError, StopIteration):
            continue
    # 处理已删除的实验（ID不在文件系统中）
    deleted_ids = set(existing_problems.keys()) - current_ids
    if deleted_ids:
        Problem.query.filter(Problem.id.in_(deleted_ids)).delete(
            synchronize_session=False)
    db.session.commit()


# ---------- 获取Prob列表 ----------
@app.route('/problems', methods=['GET'])
def getProblems():
    """获取问题列表，返回ID、标题、难度和标签"""
    problems = Problem.query.all()
    # 构建响应数据结构
    problems_list = [{
            "id": p.id,
            "title": p.title,
            "difficulty": p.difficulty,
            "tags": p.tags.split(',') if p.tags else []  # 将字符串转换为数组
        }for p in problems]
    return jsonify(problems_list)


# ---------- 获取单个Prob详情 ----------
@app.route('/problems/<int:id>', methods=['GET'])
def getProblem(id):
    """获取单个问题详情，返回ID、标题、文档、难度、标签、代码模板"""
    problem = Problem.query.get(id)
    if not problem:
        return jsonify({"error": "Problem not found"}), 404
    # 构建响应数据
    response_data = {
        "id": problem.id,
        "title": problem.title,
        "documentation": problem.description,  # 完整文档内容
        "difficulty": problem.difficulty,
        "tags": problem.tags.split(',') if problem.tags else [],  # 转换为数组
        "code_template": problem.code_temp  # 代码编辑器初始内容
    }
    return jsonify(response_data)


# ---------- 获取用户历史提交记录 ----------
@app.route('/users/<int:user_id>/submissions', methods=['GET'])
def getUserSubmissions(user_id):
    """获取提交历史，返回用户的历史提交ID，status，日期"""
    # 验证存在性
    if not User.query.get(user_id):
        return jsonify({"error": "用户不存在"}), 404
    # 查询提交记录（仅获取必要字段）
    submissions = Submission.query.with_entities(
        Submission.id,
        Submission.created_at,
        Submission.status
    ).filter_by(user_id=user_id).order_by(Submission.created_at.desc()).all()
    # 构建响应数据
    return jsonify([{
        "uuid": sub.id,
        "date": sub.created_at.isoformat(),
        "status": sub.status
    } for sub in submissions])


if __name__=='__main__':
    app.run()


with app.app_context():
    db.create_all()
    updateProblems()