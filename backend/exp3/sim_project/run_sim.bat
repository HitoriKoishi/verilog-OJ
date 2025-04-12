@echo off
setlocal enabledelayedexpansion

:: 错误码定义
set NO_ERROR=0
set ERROR_COMPILE_FAIL=1
set ERROR_SIM_LOAD_FAIL=2
set ERROR_SIM_RUN_FAIL=3
set ERROR_SIM_TIMEOUT=4
set ERROR_MISMATCH=5

:: 配置参数
set TB_MODULE=test_bench
set SRC_LIST=sim_file_list.f
set LOG_FILE=simulation.log
set VCD_FILE=waveform.vcd
set OBJ_FILE=sim_exec
set TIMEOUT_SEC=6
set ERROR_CODE=%NO_ERROR%

:: 清理旧文件
del "%VCD_FILE%"
del %LOG_FILE%

:: 编译阶段
echo INFO: Start Sim at %TIME% >> %LOG_FILE%
echo [1/3] Compiling... >> %LOG_FILE%
iverilog -o sim_exec -s %TB_MODULE% -f %SRC_LIST% >> %LOG_FILE% 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Compilation failed >> %LOG_FILE%
    set ERROR_CODE=%ERROR_COMPILE_FAIL%
    goto END
)

:: 仿真阶段（带超时）
echo [2/3] Running simulation (timeout: %TIMEOUT_SEC%s)... >> %LOG_FILE%
powershell -Command "$job = Start-Process -FilePath 'vvp' -ArgumentList '-n %OBJ_FILE%' -NoNewWindow -PassThru; try { $job | Wait-Process -Timeout %TIMEOUT_SEC% -ErrorAction Stop } catch { if ($_.Exception -is [System.TimeoutException]) { exit %ERROR_SIM_TIMEOUT% } else { exit $job.ExitCode } }" >> %LOG_FILE% 2>&1
set SIM_ERROR_CODE=!ERRORLEVEL!

:: 处理仿真结果
if %SIM_ERROR_CODE% equ %ERROR_SIM_TIMEOUT% (
    echo ERROR: Simulation timeout >> %LOG_FILE%
    set ERROR_CODE=%ERROR_SIM_TIMEOUT%
    goto END
) else if %SIM_ERROR_CODE% neq 0 (
    echo ERROR: Simulation runtime error >> %LOG_FILE%
    set ERROR_CODE=%ERROR_SIM_RUN_FAIL%
    goto END
)

:: 结果检查
echo [3/3] Checking results... >> %LOG_FILE%
findstr /C:"TEST FAILED" %LOG_FILE% >nul
if %ERRORLEVEL% equ 0 (
    echo ERROR: Output mismatch >> %LOG_FILE%
    set ERROR_CODE=%ERROR_MISMATCH%
    goto END
)

if not exist "%VCD_FILE%" (
    echo ERROR: VCD file not generated >> %LOG_FILE%
    set ERROR_CODE=%ERROR_SIM_LOAD_FAIL%
    goto END
)

findstr /C:"TEST PASSED" %LOG_FILE% >nul
if %ERRORLEVEL% equ 0 (
    echo INFO: Simulation PASSED >> %LOG_FILE%
    set ERROR_CODE=%NO_ERROR%
    goto END
) else (
    echo INFO: Simulation no result >> %LOG_FILE%
    set ERROR_CODE=%NO_ERROR%
    goto END
)


:END
echo INFO: End Sim at %TIME% >> %LOG_FILE%
del %OBJ_FILE%
exit %ERROR_CODE%