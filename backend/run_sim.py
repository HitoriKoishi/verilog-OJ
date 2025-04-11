import subprocess
import sys
from pathlib import Path
from enum import IntEnum
import os

class ErrorCode(IntEnum):
    NO_ERROR            = 0
    ERROR_COMPILE_FAIL  = 1
    ERROR_SIM_LOAD_FAIL = 2
    ERROR_SIM_RUN_FAIL  = 3
    ERROR_SIM_TIMEOUT   = 4
    ERROR_MISMATCH      = 5
    ERROR_BAT_NOT_FOUND = 6
    ERROR_UNKNOWN       = 7

def run_simulation(expnum: int, timeout = 60) -> int:
    current_dir = os.path.dirname(__file__)
    os.chdir(str(current_dir)+"\\exp"+str(expnum)+"\\sim_project")
    bat_file = Path("run_sim.bat")

    if not bat_file.exists():
        print(f"Error: Batch file {bat_file} not found!")
        return ErrorCode.ERROR_BAT_NOT_FOUND
    try:
        result = subprocess.run(
            ["run_sim.bat"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout
        )
        return ErrorCode(result.returncode)

    except subprocess.TimeoutExpired:
        print(f"Error: Simulation timeout ({timeout}s)")
        return ErrorCode.ERROR_SIM_TIMEOUT
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return ErrorCode.ERROR_UNKNOWN

"""
exit_code = run_simulation(expnum=1)
print(f"Simulation finished with code: {exit_code.name}({exit_code.value})")
"""

if __name__ == "__main__":
    # 示例调用：实验编号1
    exit_code = run_simulation(expnum=1)
    print(f"Simulation finished with code: {exit_code.name}({exit_code.value})")
    sys.exit(exit_code.value)