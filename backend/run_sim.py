import subprocess
import os
from pathlib import Path
from enum import IntEnum
from datetime import datetime

class ErrorCode(IntEnum):
    SUCCESS             = 0
    ERROR_COMPILE_FAIL  = 1
    ERROR_SIM_LOAD_FAIL = 2
    ERROR_SIM_RUN_FAIL  = 3
    ERROR_SIM_TIMEOUT   = 4
    ERROR_MISMATCH      = 5
    ERROR_BAT_NOT_FOUND = 6
    ERROR_UNKNOWN       = 7

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