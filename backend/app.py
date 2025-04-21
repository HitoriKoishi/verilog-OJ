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
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://localhost:1234"], "supports_credentials": True}})
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
from app_learningPath.routes import learningPath_bp
from app_admin.routes import admin_bp  # 导入管理员蓝图
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(problem_bp, url_prefix='/problem')
app.register_blueprint(submit_bp, url_prefix='/submission')
app.register_blueprint(learningPath_bp, url_prefix='/learningPath')
app.register_blueprint(admin_bp, url_prefix='/admin')  # 注册管理员蓝图

# 启动后台线程并传递 app 实例
simulation_thread = threading.Thread(target=simulation_worker, args=(app,), daemon=True)
simulation_thread.start()

# ---------- 更新Prob数据库 ----------
def updateProblems():
    """根据题目文件夹更新数据库"""
    # 获取现有问题映射 {id: problem_obj}
    existing_problems = {p.id: p for p in Problem.query.all()}
    current_ids = set()
    
    # 扫描所有题目文件夹
    for prob_dir in PROB_DIR.glob("*"):
        if not prob_dir.is_dir():
            continue
            
        doc_dir = prob_dir / "doc"
        doc_path = doc_dir / "doc.md"
        temp_code_path = doc_dir / "temp_module.v"
        
        if not doc_path.exists():
            continue
            
        try:
            with open(doc_path, "r", encoding="utf-8") as f:
                doc_content = f.read()
                
            # 分割文档内容为行
            lines = doc_content.splitlines()
            
            # 提取信息
            title = ""
            prob_id = None
            difficulty = "简单"
            tags = ""
            pre_problems = ""
            next_problems = ""
            new_content_lines = []
            
            # 处理文档内容
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith("# "):
                    title = line.strip("# \n")
                elif line.startswith("ID："):
                    try:
                        prob_id = int(line[3:].strip())
                        current_ids.add(prob_id)
                    except ValueError:
                        continue
                elif line.startswith("难度："):
                    difficulty = line[3:].strip()
                elif line.startswith("标签："):
                    tags = line[3:].strip()
                elif line.startswith("前置："):
                    pre_problems = line[3:].strip()
                elif line.startswith("后置："):
                    next_problems = line[3:].strip()
                elif line.startswith("## "):
                    new_content_lines.extend(lines[i:])
                    break
                i += 1
                
            if prob_id is None:
                continue
                
            # 组合新的文档内容
            new_doc_content = "\n".join(new_content_lines)
            
            # 读取代码模板
            code_temp = ""
            if temp_code_path.exists():
                with open(temp_code_path, "r", encoding="utf-8") as f:
                    code_temp = f.read()
                    
            # 更新或创建记录
            if prob_id in existing_problems:
                problem = existing_problems[prob_id]
                problem.title = title
                problem.folder_path = str(prob_dir.relative_to(PROB_DIR))
                problem.description = new_doc_content
                problem.code_temp = code_temp
                problem.difficulty = difficulty
                problem.tags = tags
                problem.pre_problems = pre_problems
                problem.next_problems = next_problems
            else:
                problem = Problem(
                    id=prob_id,
                    folder_path=str(prob_dir.relative_to(PROB_DIR)),
                    title=title,
                    description=new_doc_content,
                    code_temp=code_temp,
                    difficulty=difficulty,
                    tags=tags,
                    pre_problems=pre_problems,
                    next_problems=next_problems
                )
                db.session.add(problem)
        except Exception as e:
            print(f"处理题目 {prob_dir.name} 时出错: {str(e)}")
            continue
            
    # 处理已删除的题目
    deleted_ids = set(existing_problems.keys()) - current_ids
    if deleted_ids:
        Problem.query.filter(Problem.id.in_(deleted_ids)).delete(
            synchronize_session=False)
    db.session.commit()

if __name__=='__main__':
    with app.app_context():
        db.create_all()
        updateProblems()
    app.run(host='0.0.0.0', port=5000)  # 修改为监听所有地址

@atexit.register
def cleanup():
    """清理后台线程"""
    simulation_queue.put(None)  # 向队列发送结束信号
    simulation_thread.join()