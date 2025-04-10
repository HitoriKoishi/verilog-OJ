import subprocess
import sys
from pathlib import Path
from enum import IntEnum

class ErrorCode(IntEnum):
    NO_ERROR            = 0
    ERROR_COMPILE_FAIL  = 1
    ERROR_SIM_LOAD_FAIL = 2
    ERROR_SIM_RUN_FAIL  = 3
    ERROR_SIM_TIMEOUT   = 4
    ERROR_MISMATCH      = 5
    ERROR_TCL_NOT_FOUND = 6
    ERROR_UNKNOWN       = 7

def run_simulation(expnum:int, vsim_timeout:int) -> int:
    work_path = "exp"+str(expnum)+"/sim_project/"
    tcl_script = "ctrl_phy_sim.tcl"
    vsim_path = "vsim"
    if not Path(work_path+tcl_script).exists():
        print(f"Error: TCL script {work_path+tcl_script} not found!")
        return ErrorCode.ERROR_TCL_NOT_FOUND
    cmd = [
        vsim_path,
        "-c",           # 命令行模式
        "-do",          # 执行TCL命令
        f"source {tcl_script}; quit -f"
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=work_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=False,
            timeout=vsim_timeout  # 10s超时
        )
        # 转换返回码为枚举类型
        try:
            return ErrorCode(result.returncode)
        except ValueError:
            print(f"Unknown return code: {result.returncode}")
            return ErrorCode.ERROR_UNKNOWN     
    except subprocess.TimeoutExpired:
        print("Error: Simulation timeout ("+str(vsim_timeout)+"s)")
        return ErrorCode.ERROR_SIM_TIMEOUT
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return ErrorCode.ERROR_UNKNOWN

if __name__ == "__main__":
    exit_code = run_simulation(1, 10) #exp1, timeout 10s
    print(f"Simulation finished with code: {exit_code.name}({exit_code.value})")
    sys.exit(exit_code)