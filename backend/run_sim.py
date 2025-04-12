import subprocess
import sys
import shutil
from pathlib import Path
from enum import IntEnum
import os

# 在配置中添加存储根目录
BASE_DIR = Path(__file__).parent
SUBMISSION_DATA_ROOT = BASE_DIR / "submissions_data"

class SimulationResult:
    def __init__(self):
        self.error_code = ErrorCode.ERROR_UNKNOWN
        self.log_path = ""
        self.waveform_path = ""

class ErrorCode(IntEnum):
    SUCCESS             = 0
    ERROR_COMPILE_FAIL  = 1
    ERROR_SIM_LOAD_FAIL = 2
    ERROR_SIM_RUN_FAIL  = 3
    ERROR_SIM_TIMEOUT   = 4
    ERROR_MISMATCH      = 5
    ERROR_BAT_NOT_FOUND = 6
    ERROR_UNKNOWN       = 7

def run_simulation(expnum: int, submission_id: str) -> SimulationResult:
    result = SimulationResult()
    sim_project_dir = BASE_DIR / f"exp{expnum}" / "sim_project"
    bat_file = sim_project_dir / "run_sim.bat"
    # 准备目标存储目录
    save_dir = BASE_DIR / "sub_data"
    save_dir.mkdir(parents=True, exist_ok=True)
    try:
        # 执行仿真过程
        process = subprocess.run(
            [str(bat_file)],
            cwd=sim_project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=60,
            encoding='utf-8',
            errors='replace'
        )
        # 处理生成的文件
        result.error_code = ErrorCode(process.returncode)
        # 移动日志文件
        src_log = sim_project_dir / "simulation.log"
        src_vcd = sim_project_dir / "waveform.vcd"
        if src_log.exists():
            dest_log = save_dir / f"sim_{submission_id[:8]}.log"
            shutil.move(str(src_log), str(dest_log))
            result.log_path = str(dest_log.relative_to(BASE_DIR))
        if src_vcd.exists():
            dest_vcd = save_dir / f"wave_{submission_id[:8]}.vcd"
            shutil.move(str(src_vcd), str(dest_vcd))
            result.waveform_path = str(dest_vcd.relative_to(BASE_DIR))
    except Exception as e:
        result.error_code = ErrorCode.ERROR_UNKNOWN
        result.log_path = ""
        result.waveform_path = ""
    return result

if __name__ == "__main__":
    # 示例调用：实验编号1
    sim_result = run_simulation(expnum=1, submission_id="000")
    print(sim_result.error_code)
    print(sim_result.log_path)
    print(sim_result.waveform_path)