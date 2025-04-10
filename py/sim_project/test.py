import subprocess
import sys
from pathlib import Path

def run_simulation(tcl_script: str) -> int:
    """
    执行ModelSim仿真并返回退出码
    :param tcl_script: TCL脚本路径
    :return: 0=成功，1=失败
    """
    # 验证ModelSim可执行路径
    vsim_path = "vsim"  # 假设已添加到环境变量
    if not Path(tcl_script).exists():
        print(f"Error: TCL script {tcl_script} not found!")
        return 1

    # 构造执行命令
    cmd = [
        vsim_path,
        "-c",           # 命令行模式
        "-do",          # 执行TCL命令
        f"source {tcl_script}; quit -f",  # 必须强制退出
        "-l", "vsim.log"# 保存详细日志
    ]

    # 静默执行
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
            text=True,
            timeout=300  # 最多等待5分钟
        )
        return 0 if result.returncode == 0 else 1
    except subprocess.CalledProcessError as e:
        print(f"Simulation failed with code {e.returncode}")
        return 1
    except subprocess.TimeoutExpired:
        print("Simulation timeout!")
        return 1

if __name__ == "__main__":
    exit_code = run_simulation("ctrl_phy_sim.tcl")
    sys.exit(exit_code)