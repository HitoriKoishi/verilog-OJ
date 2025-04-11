from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
import json
from pathlib import Path

# 导入 sim_run 模块
from backend.sim_run import run_simulation as sim_run_verilog
from backend.sim_run import ErrorCode

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.secret_key = 'verilog-oj-secret-key'

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent

# 题目数据
PROBLEMS = [
    {
        'id': 1,
        'title': '简单异或触发器',
        'description': '''
        <h3>问题描述</h3>
        <p>实现一个简单的异或触发器，该触发器在时钟上升沿或复位下降沿工作。</p>
        <h3>模块接口</h3>
        <pre>module user_module (
    input clk,
    input rstn,
    input in, 
    output reg out
);</pre>
        <h3>功能要求</h3>
        <p>1. 当rstn为低电平时，输出out复位为0</p>
        <p>2. 当rstn为高电平时，在时钟上升沿，输出out等于输入in与前一状态out的异或</p>
        ''',
        'test_bench': 'test_bench.v',
        'template': '''module user_module (
    input clk,
    input rstn,
    input in, 
    output reg out
);
// 在此处添加您的代码
// ...

endmodule'''
    }
]

@app.route('/')
def index():
    return render_template('index.html', problems=PROBLEMS)

@app.route('/problem/<int:problem_id>')
def problem(problem_id):
    # 查找对应的题目
    problem = next((p for p in PROBLEMS if p['id'] == problem_id), None)
    if not problem:
        flash('题目不存在！', 'danger')
        return redirect(url_for('index'))
    
    return render_template('problem.html', problem=problem)

@app.route('/submit/<int:problem_id>', methods=['POST'])
def submit(problem_id):
    # 查找对应的题目
    problem = next((p for p in PROBLEMS if p['id'] == problem_id), None)
    if not problem:
        return jsonify({'success': False, 'message': '题目不存在！'})
    
    # 获取用户提交的代码
    code = request.form.get('code', '')
    if not code:
        return jsonify({'success': False, 'message': '代码不能为空！'})
    
    try:
        # 保存用户代码到test_module目录
        user_module_path = BASE_DIR / 'backend' / f'exp{problem_id}' / 'test_module' / 'user_module.v'
        with open(user_module_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # 运行模拟
        result, status_message, log_output = run_simulation(problem_id)
        
        # 解析波形文件
        sim_project_dir = BASE_DIR / 'backend' / f'exp{problem_id}' / 'sim_project'
        waveform_path = sim_project_dir / 'waveform.vcd'
        waveform_data = parse_waveform(waveform_path)
        
        return jsonify({
            'success': True, 
            'result': result,
            'message': status_message,
            'log': log_output,
            'waveform': waveform_data
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'评测异常：{str(e)}'})

def run_simulation(problem_id, vsim_timeout=10):
    """运行Verilog仿真并返回结果"""
    # 调用 backend/sim_run.py 中的 run_simulation 函数
    error_code = sim_run_verilog(problem_id, vsim_timeout)
    
    # 读取日志文件
    log_path = BASE_DIR / 'backend' / f'exp{problem_id}' / 'sim_project' / 'simulation.log'
    log_output = "日志文件未生成"
    
    if log_path.exists():
        try:
            with open(log_path, 'r', errors='replace') as f:
                log_output = f.read()
        except Exception as e:
            log_output = f"读取日志文件出错: {str(e)}"
    
    # 根据错误码返回结果
    error_messages = {
        ErrorCode.NO_ERROR: "仿真成功，结果正确",
        ErrorCode.ERROR_COMPILE_FAIL: "编译错误，请检查代码语法",
        ErrorCode.ERROR_SIM_LOAD_FAIL: "仿真启动失败，请检查代码",
        ErrorCode.ERROR_SIM_RUN_FAIL: "仿真运行错误，请检查代码逻辑",
        ErrorCode.ERROR_SIM_TIMEOUT: "仿真超时，请检查是否有死循环",
        ErrorCode.ERROR_MISMATCH: "输出与参考不匹配，请检查代码逻辑",
        ErrorCode.ERROR_TCL_NOT_FOUND: "TCL脚本未找到，系统错误",
        ErrorCode.ERROR_UNKNOWN: "未知错误，请联系管理员"
    }
    
    status_message = error_messages.get(error_code, f"未知状态码: {error_code}")
    
    if error_code == ErrorCode.NO_ERROR:
        return "通过", status_message, log_output
    else:
        return "失败", status_message, log_output

def parse_waveform(vcd_path):
    """从VCD文件解析波形数据为前端可用的格式"""
    if not vcd_path.exists():
        return {'error': '波形文件不存在，仿真可能失败'}
    
    try:
        # 存储信号映射关系 (变量名 -> 信号代码)
        signal_map = {}
        # 存储解析后的信号数据
        signals = {
            'clk': [],
            'rstn': [],
            'refrence_in': [],
            'your_out': [],
            'refrence_out': [],
            'mismatch': []
        }
        
        with open(vcd_path, 'r', errors='replace') as f:
            lines = f.readlines()
        
        # 第一轮扫描，建立变量名和信号代码的映射
        in_vars_section = False
        for line in lines:
            line = line.strip()
            
            # 变量定义部分开始
            if line.startswith('$scope'):
                in_vars_section = True
                continue
            
            # 变量定义部分结束
            if line.startswith('$upscope') or line.startswith('$enddefinitions'):
                in_vars_section = False
                continue
            
            # 解析变量定义
            if in_vars_section and line.startswith('$var'):
                parts = line.split()
                if len(parts) >= 5:
                    var_code = parts[3]  # 信号代码
                    var_name = parts[4]  # 变量名
                    
                    # 匹配我们关心的信号
                    if var_name == 'clk':
                        signal_map['clk'] = var_code
                    elif var_name == 'rstn':
                        signal_map['rstn'] = var_code
                    elif var_name == 'refrence_in':
                        signal_map['refrence_in'] = var_code
                    elif var_name == 'your_out':
                        signal_map['your_out'] = var_code
                    elif var_name == 'refrence_out':
                        signal_map['refrence_out'] = var_code
                    elif var_name == 'mismath_out':
                        signal_map['mismatch'] = var_code
        
        # 第二轮扫描，提取时间-值数据对
        current_time = 0
        for line in lines:
            line = line.strip()
            
            # 时间戳行
            if line.startswith('#'):
                try:
                    current_time = int(line[1:])
                except ValueError:
                    continue
            
            # 值变化行 (格式: 值 信号代码)
            elif len(line) >= 2 and line[0] in "01xz" and line[1:] in signal_map.values():
                value = line[0]
                signal_code = line[1:]
                
                # 反向查找信号名
                for signal_name, code in signal_map.items():
                    if code == signal_code:
                        signals[signal_name].append((current_time, value))
                        break
        
        return signals
    except Exception as e:
        return {'error': f'解析波形文件出错: {str(e)}'}

if __name__ == '__main__':
    app.run(debug=True)
