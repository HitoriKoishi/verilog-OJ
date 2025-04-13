# Verilog 在线评测系统 - 后端
python后端

仿真环境基于开源仿真软件iverilog，相比之前使用的modelsim，优点是仿真速度很快，开源轻量；缺点是语法支持不完备。

## 仿真环境搭建

python调取的是``backend/iverilog``，一般来说不用再下载了。

*Linux环境下需要自行下载iverilog，修改model.py里的``IVERILOG``和``VVP``。*

## 目录结构

```
│   README.md                   README
|   requirements.txt            requirements
|   app.py                      后端py文件
|   exts.py                     数据库引用
|   models.py                   模块引用
│
├───iverilog                    iverilog库
│
├───app_auth
|       routes.py               用户管理接口
│
├───app_problem
|       routes.py               题目管理接口
│
├───app_submit
|       routes.py               提交管理接口
│
├───instance
|       example.db              数据库
|
├───sub_data                    提交记录文件夹
│       sim_<submit_id>.log         submit_id的日志
│       wave_<submit_id>.vcd        submit_id的波形 
│
└───Prob                        
    ├───exp1                        实验1
    │   ├───doc                         文档
    │   │       doc.md                      实验1文档
    │   │       temp_module.v               实验1代码编辑器暂存内容
    │   └───project                     仿真工程
    │           ctrl_phy_sim.bat            bat脚本
    │           sim_file_list.f             编译文件列表
    │           test_bench.v                测试用例
    │           ref_module.v                标准参考模块
    ├───exp2                        实验2
    |   ...
```

## 函数返回值
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

仿真会在``backend``内的一个临时文件夹里进行，运行完毕后转移日志和波形文件，随后删除。

### doc.md

### temp_module.v
temp_module.v 是用户打开题目后代码编辑器内暂存的内容

### sim_file_list.f
需要iverilog编译的文件列表，以sim_project作为根目录。不可以使用通配符，注意文件最后留一行

### test_bench
1. 模块名必须为test_bench();不可更改
2. 需要使用$dump系统函数生成vcd波形
3. 注意控制仿真时间，减小波形文件大小
4. 使用$display函数可以打印在log日志上
5. bat脚本通过判断log日志中的"TEST FAILED"或"TEST PASSED"字符串确认仿真结果，因此需要test_bench判断仿真是否通过并display输出结果。

### ref_module.v
参考模块，提供该题目的标准答案