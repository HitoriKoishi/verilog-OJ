# verilog-OJ PYTHON
python后端

目录结构

```
│   README.md
│   sim_run.py
│
├───exp1                        实验1
│   ├───sim_project                 仿真工程
│   │       ctrl_phy_sim.tcl            tcl脚本
│   │       simulation.log              log日志
│   │       sim_file_list.f             仿真文件列表
│   │       waveform.vcd                vcd波形
│   │
│   ├───test_bench              仿真文件夹
│   │       test_bench.v            测试用例
│   │
│   └───test_module             被测文件夹
│           ref_module.v            标准参考模块
│           user_module.v           用户上传模块
│
├───exp2                        实验2
|...
```
执行`sim_run.py`或调用`run_simulation(expnum:int, vsim_timeout:int)`函数

执行完毕后在对应的`sim_project`文件夹下生成log日志和vcd波形（如仿真成功）

函数返回值：
```
    NO_ERROR            = 0     # 仿真通过
    ERROR_COMPILE_FAIL  = 1     # 编译错误，检查语法
    ERROR_SIM_LOAD_FAIL = 2     # 仿真启动失败，检查语法
    ERROR_SIM_RUN_FAIL  = 3     # 仿真非自然结束
    ERROR_SIM_TIMEOUT   = 4     # 仿真超时
    ERROR_MISMATCH      = 5     # 波形不匹配
    ERROR_TCL_NOT_FOUND = 6     # 未找到TCL脚本
    ERROR_UNKNOWN       = 7     # 未知错误
```

