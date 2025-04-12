from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_cors import CORS  # 导入CORS
import subprocess
from datetime import datetime
from pathlib import Path
from models import User, UserCode, ErrorCode, Problem, Submission, SubmissionStatus, SimulationResult
import tempfile
import shutil
from exts import db


# 项目根目录
BASE_DIR = Path(__file__).resolve().parent
PROB_DIR = BASE_DIR/"Prob"

def load_config(app):
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173", "supports_credentials": True}})
    app.secret_key = 'verilog-oj-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # 使用 SQLite 数据库
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app = Flask(__name__)
load_config(app)
db.init_app(app)

# 初始化登录管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/user/login'

@login_manager.user_loader
def loaduser(user_id):
    return User.query.get(int(user_id))

from app_auth.routes import user_bp
from app_problem.routes import problem_bp
from app_submit.routes import submit_bp
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(problem_bp, url_prefix='/problems')
app.register_blueprint(submit_bp, url_prefix='/submissions')

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

def sim_run_verilog(submission_id: int) -> SimulationResult:
    result = SimulationResult()
    submission = Submission.query.get(submission_id)
    if not submission:
        result.error_code = ErrorCode.ERROR_UNKNOWN
        return result
    # 获取 problem_id 和对应的 project 目录
    problem_id = submission.problem_id
    project_dir = PROB_DIR / f"exp{problem_id}" / "project"
    if not project_dir.exists():
        result.error_code = ErrorCode.ERROR_UNKNOWN
        return result
    # 创建临时文件夹
    with tempfile.TemporaryDirectory(dir=BASE_DIR) as temp_dir:
        temp_dir_path = Path(BASE_DIR/temp_dir)
        # 将 problem_id 对应的 project 文件夹内容复制到临时文件夹
        shutil.copytree(project_dir, temp_dir_path, dirs_exist_ok=True)
        # 创建 user_module.v 文件，将用户代码写入
        user_module_path = temp_dir_path / "user_module.v"
        with open(user_module_path, 'w', encoding='utf-8') as f:
            f.write(submission.code)
        # 准备目标存储目录
        save_dir = BASE_DIR / "sub_data"
        save_dir.mkdir(parents=True, exist_ok=True)
        try:
            # 调用 run_simulation 函数执行仿真
            error_code = run_simulation(temp_dir_path, timeout_sec=60)
            result.error_code = error_code
            # 处理生成的文件
            src_log = temp_dir_path / "simulation.log"
            src_vcd = temp_dir_path / "waveform.vcd"
            if src_log.exists():
                dest_log = save_dir / f"sim_{str(submission_id)}.log"
                shutil.move(str(src_log), str(dest_log))
                result.log_path = str(dest_log.relative_to(BASE_DIR))
            if src_vcd.exists():
                dest_vcd = save_dir / f"wave_{str(submission_id)}.vcd"
                shutil.move(str(src_vcd), str(dest_vcd))
                result.waveform_path = str(dest_vcd.relative_to(BASE_DIR))
        except Exception as e:
            result.error_code = ErrorCode.ERROR_UNKNOWN
            result.log_path = ""
            result.waveform_path = ""
    # 临时文件夹会在 with 语句结束时自动删除
    return result

def run_simulation(base_dir: Path, timeout_sec: int = 6) -> ErrorCode:
    """
    Python 函数版本的仿真执行逻辑
    :param base_dir: 仿真项目的根目录
    :param timeout_sec: 仿真超时时间（秒）
    :return: ErrorCode 枚举值
    """
    # 配置参数
    tb_module = "test_bench"
    log_file =  Path(base_dir/"simulation.log")
    vcd_file =  Path(base_dir/"waveform.vcd")
    obj_file =  Path(base_dir/"sim_exec")
    error_code = ErrorCode.SUCCESS

    # 清理旧文件
    if vcd_file.exists():
        vcd_file.unlink()
    if log_file.exists():
        log_file.unlink()

    # 编译阶段
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"INFO: Start Sim at {datetime.now().isoformat()}\n")
        log.write("[1/3] Compiling...\n")
        try:
            subprocess.run(
                ["iverilog", "-o", "sim_exec", "-s", tb_module, "-f", "sim_file_list.f"],
                stdout=log,
                stderr=subprocess.STDOUT,
                check=True,
                cwd=base_dir
            )
        except subprocess.CalledProcessError:
            log.write("ERROR: Compilation failed\n")
            return ErrorCode.ERROR_COMPILE_FAIL

    # 仿真阶段（带超时）
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"[2/3] Running simulation (timeout: {timeout_sec}s)...\n")
        try:
            subprocess.run(
                ["vvp", "-n", "sim_exec"],
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=timeout_sec,
                cwd=base_dir
            )
        except subprocess.TimeoutExpired:
            log.write("ERROR: Simulation timeout\n")
            return ErrorCode.ERROR_SIM_TIMEOUT
        except subprocess.CalledProcessError:
            log.write("ERROR: Simulation runtime error\n")
            return ErrorCode.ERROR_SIM_RUN_FAIL

    # 结果检查
    with open(log_file, "a", encoding="utf-8") as log:
        log.write("[3/3] Checking results...\n")
        try:
            with open(log_file, "r", encoding="utf-8") as log_content:
                log_data = log_content.read()
                if "TEST FAILED" in log_data:
                    log.write("ERROR: Output mismatch\n")
                    return ErrorCode.ERROR_MISMATCH
                if not vcd_file.exists():
                    log.write("ERROR: VCD file not generated\n")
                    return ErrorCode.ERROR_SIM_LOAD_FAIL
                if "TEST PASSED" in log_data:
                    log.write("INFO: Simulation PASSED\n")
                    return ErrorCode.SUCCESS
        except Exception as e:
            log.write(f"ERROR: Unexpected error during result check: {e}\n")
            return ErrorCode.ERROR_SIM_RUN_FAIL

    # 清理生成的文件
    if obj_file.exists():
        obj_file.unlink()

    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"INFO: End Sim at {datetime.now().isoformat()}\n")

    return error_code

if __name__=='__main__':
    app.run()

with app.app_context():
    db.create_all()
    updateProblems()