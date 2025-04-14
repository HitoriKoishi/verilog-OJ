from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_cors import CORS  # 导入CORS
from models import User, UserCode, ErrorCode, Problem, Submission, SubmissionStatus, SimulationResult
from exts import db
from models import BASE_DIR, PROB_DIR, login_required
from app_submit.run_sim import simulation_queue, simulation_worker
import threading
import atexit



def load_config(app):
    CORS(app, resources=r'/*', supports_credentials=True)
    app.secret_key = 'verilog-oj-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # 使用 SQLite 数据库
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app = Flask(__name__)
load_config(app)
db.init_app(app)

# 初始化登录管理
login_manager = LoginManager()
login_manager.login_view = '/user/login'
login_manager.init_app(app)

@login_manager.user_loader
def loaduser(user_id):
    return User.query.get(int(user_id))

from app_auth.routes import user_bp
from app_problem.routes import problem_bp
from app_submit.routes import submit_bp
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(problem_bp, url_prefix='/problem')
app.register_blueprint(submit_bp, url_prefix='/submission')

# 启动后台线程并传递 app 实例
simulation_thread = threading.Thread(target=simulation_worker, args=(app,), daemon=True)
simulation_thread.start()

# ---------- 更新Prob数据库 ----------
def updateProblems():
    """根据exp文件夹更新数据库"""
    # 获取现有问题映射 {id: problem_obj}
    existing_problems = {p.id: p for p in Problem.query.all()}
    current_ids = set()
    # 扫描 exp 开头的文件夹
    for exp_dir in PROB_DIR.glob("exp*"):
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

if __name__=='__main__':
    with app.app_context():
        db.create_all()
        updateProblems()
    app.run(host='0.0.0.0',port=5000)

@atexit.register
def cleanup():
    """清理后台线程"""
    simulation_queue.put(None)  # 向队列发送结束信号
    simulation_thread.join()