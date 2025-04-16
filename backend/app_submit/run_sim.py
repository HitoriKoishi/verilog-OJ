from models import Submission
from models import ErrorCode, SimulationResult
from models import SubmissionStatus
from flask import current_app
from pathlib import Path
import shutil
import subprocess
import tempfile
from datetime import datetime
from models import BASE_DIR, PROB_DIR, IVERILOG, VVP
from queue import Queue
from exts import db

# 创建任务队列
simulation_queue = Queue()

def simulation_worker(app):
    """后台线程：从队列中获取任务并执行仿真"""
    with app.app_context():  # 手动激活应用上下文
        while True:
            try:
                print("等待仿真任务...")
                # 从队列中获取 submission_id
                submission_id = simulation_queue.get()
                if submission_id is None:
                    break  # 退出线程
                # 获取 submission 对象
                submission = Submission.query.get(submission_id)
                if not submission:
                    continue
                # 更新状态为 RUNNING
                submission.status = SubmissionStatus.RUNNING
                db.session.commit()
                print(f"开始仿真任务: {submission_id}")
                # 执行仿真
                try:
                    sim_result = sim_run_verilog(submission_id)
                    submission.status = SubmissionStatus.SUCCESS if sim_result.error_code == ErrorCode.SUCCESS else SubmissionStatus.FAILED
                    submission.error_code = sim_result.error_code.name
                    submission.log_path = sim_result.log_path
                    submission.waveform_path = sim_result.waveform_path
                except Exception as e:
                    # 仿真失败
                    submission.status = SubmissionStatus.FAILED
                    submission.error_code = str(e)
                    submission.log_path = ""
                    submission.waveform_path = ""
                    print(f"仿真任务异常: {e}")
                finally:
                    db.session.commit()
                    print(f"仿真任务完成: {submission_id}, 状态: {submission.status}")
            except Exception as e:
                print(f"仿真任务执行失败: {e}")
            finally:
                simulation_queue.task_done()

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
            error_code = run_simulation(temp_dir_path, timeout_sec=6)
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
            print(e)
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
                [IVERILOG, "-o", "sim_exec", "-s", tb_module, "-f", "sim_file_list.f"],
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=timeout_sec,
                check=True,
                shell=True,
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
                [VVP, "-n", "sim_exec"],
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=timeout_sec,
                shell=True,
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
                    log.write("INFO: VCD file not generated\n")
                    # return ErrorCode.ERROR_SIM_LOAD_FAIL
                if "TEST PASSED" in log_data:
                    log.write("INFO: Simulation PASSED\n")
                    return ErrorCode.SUCCESS
                else:
                    log.write("ERROR: Unknown simulation result\n")
                    return ErrorCode.ERROR_UNKNOWN
        except Exception as e:
            log.write(f"ERROR: Unexpected error during result check: {e}\n")
            return ErrorCode.ERROR_SIM_RUN_FAIL

    # 清理生成的文件
    if obj_file.exists():
        obj_file.unlink()

    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"INFO: End Sim at {datetime.now().isoformat()}\n")

    return error_code