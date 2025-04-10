from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
import tempfile
import subprocess
import json
import shutil
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'verilog-oj-secret-key'

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent
# 测试模块目录
TEST_MODULE_DIR = BASE_DIR / 'py' / 'test_module'
# 仿真项目目录
SIM_PROJECT_DIR = BASE_DIR / 'py' / 'sim_project'

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
        user_module_path = TEST_MODULE_DIR / 'user_module.v'
        with open(user_module_path, 'w') as f:
            f.write(code)
        
        # 运行模拟
        result, log_output = run_simulation()
        
        # 解析波形文件
        waveform_data = parse_waveform(SIM_PROJECT_DIR / 'waveform.vcd')
        
        return jsonify({
            'success': True, 
            'result': result,
            'log': log_output,
            'waveform': waveform_data
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'评测异常：{str(e)}'})

def run_simulation():
    """运行Verilog仿真并返回结果"""
    # 切换到仿真项目目录
    os.chdir(SIM_PROJECT_DIR)
    
    # 运行测试脚本
    try:
        if os.name == 'nt':  # Windows
            process = subprocess.run(['do.bat'], 
                                    capture_output=True, 
                                    text=True,
                                    cwd=SIM_PROJECT_DIR)
        else:  # Linux/Mac
            # 确保Python脚本有执行权限
            test_script = SIM_PROJECT_DIR / 'test.py'
            os.chmod(test_script, 0o755)
            process = subprocess.run(['python', 'test.py'], 
                                    capture_output=True, 
                                    text=True,
                                    cwd=SIM_PROJECT_DIR)
        
        # 检查输出
        output = process.stdout + process.stderr
        if process.returncode == 0:
            return "通过", output
        else:
            return "失败", output
    except Exception as e:
        return "错误", str(e)

def parse_waveform(vcd_path):
    """从VCD文件解析波形数据为前端可用的格式"""
    # 简单实现，实际项目可能需要更复杂的VCD解析
    # 这里我们直接返回波形的文本内容，前端可以使用WaveDrom等工具渲染
    try:
        with open(vcd_path, 'r') as f:
            lines = f.readlines()[20:200]  # 仅读取一部分，避免文件过大
        
        # 解析为简单的时间-值数据对
        signals = {
            'clk': [],
            'rstn': [],
            'refrence_in': [],
            'your_out': [],
            'refrence_out': [],
            'mismatch': []
        }
        
        current_time = 0
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                current_time = int(line[1:])
            elif line and len(line) >= 2 and line[0] in "01" and line[1] in "!\"#$%&":
                value = line[0]
                signal_code = line[1]
                
                # 映射信号代码到信号名
                if signal_code == '!':
                    signals['clk'].append((current_time, value))
                elif signal_code == '"':
                    signals['rstn'].append((current_time, value))
                elif signal_code == '#':
                    signals['refrence_in'].append((current_time, value))
                elif signal_code == '$':
                    signals['your_out'].append((current_time, value))
                elif signal_code == '%':
                    signals['refrence_out'].append((current_time, value))
                elif signal_code == '&':
                    signals['mismatch'].append((current_time, value))
        
        return signals
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True)
