# verilog-OJ PYTHON
python后端

仿真环境基于开源仿真软件iverilog，Windows环境，使用bat脚本处理。相比之前使用的modelsim，优点是仿真速度很快，开源轻量；缺点是语法支持不完备。

## 仿真环境搭建：

1. https://bleyer.org/icarus/ ，下载 iverilog-v11-20210204-x64_setup.exe
2. 安装过程中选择加入PATH环境变量，安装完成后打开Terminal，输入``iverilog``检测是否加入PATH
3. gtkwave可以查看vcd波形，可选择性安装
4. 打开exp1的sim_project，运行``run_sim.bat``，查看对应simulation.log内容

## 目录结构

```
│   README.md                   README
│   sim_run.py                  仿真py文件
|   app.py                      后端py文件
│
├───exp1                        实验1
│   ├───doc                         文档
│   │       doc.md                      实验1文档
│   │       temp_module.v               实验1代码编辑器暂存内容
│   ├───sim_project                 仿真工程
│   │       ctrl_phy_sim.bat            bat脚本
│   │       sim_file_list.f             编译文件列表
│   │       simulation.log              log日志（脚本生成）
│   │       waveform.vcd                vcd波形（脚本生成）
│   │
│   ├───test_bench                  仿真文件夹
│   │       test_bench.v                测试用例
│   │
│   └───test_module                 被测文件夹
│           ref_module.v                标准参考模块
│           user_module.v               用户上传模块
│
├───exp2                        实验2
|...
```
执行`sim_run.py`或调用`run_simulation(expnum:int, vsim_timeout:int)`函数

执行完毕后在对应的`sim_project`文件夹下生成log日志和vcd波形（如仿真成功）

## 函数返回值：
```
    NO_ERROR            = 0     # 仿真通过
    ERROR_COMPILE_FAIL  = 1     # 编译错误，检查语法
    ERROR_SIM_LOAD_FAIL = 2     # 仿真启动失败，检查语法
    ERROR_SIM_RUN_FAIL  = 3     # 仿真非自然结束
    ERROR_SIM_TIMEOUT   = 4     # 仿真超时
    ERROR_MISMATCH      = 5     # 波形不匹配
    ERROR_BAT_NOT_FOUND = 6     # 未找到脚本
    ERROR_UNKNOWN       = 7     # 未知错误
```

## 注意事项

### doc.md

### temp_module.v
temp_module.v 是用户打开题目后代码编辑器内暂存的内容

### ctrl_phy_sim.bat
控制iverilog编译，仿真，识别仿真结果。非必要不更改。

### sim_file_list.f
需要iverilog编译的文件列表，以sim_project作为根目录。不可以使用通配符，注意文件最后留一行

### simulation.log
ctrl_phy_sim.bat生成的log日志

### waveform.vcd
由test_bench生成的vcd波形

### test_bench
1. 模块名必须为test_bench();不可更改
2. 需要使用$dump系统函数生成vcd波形
3. 注意控制仿真时间，减小波形文件大小
4. 使用$display函数可以打印在log日志上
5. bat脚本通过判断log日志中的"TEST FAILED"或"TEST PASSED"字符串确认仿真结果，因此需要test_bench判断仿真是否通过并display输出结果。

### ref_module.v
参考模块，提供该题目的标准答案

### user_module.v
用户上传模块，用户编辑完代码后保存在此处