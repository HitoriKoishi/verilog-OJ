import os
import tempfile
import subprocess
import shutil
import time
from pathlib import Path
from django.conf import settings

class VerilogJudge:
    """Verilog评测引擎"""
    
    def __init__(self, submission):
        self.submission = submission
        self.problem = submission.problem
        self.code = submission.code
        self.test_cases = self.problem.testcase_set.all()
        
    def run(self):
        """运行评测流程"""
        try:
            # 创建临时目录
            with tempfile.TemporaryDirectory() as temp_dir:
                # 编译代码
                compile_result = self._compile_code(temp_dir)
                if not compile_result['success']:
                    return {
                        'status': 'COMPILE_ERROR',
                        'error': compile_result['error']
                    }
                
                # 运行测试用例
                for test_case in self.test_cases:
                    test_result = self._run_test_case(temp_dir, test_case)
                    if not test_result['success']:
                        return {
                            'status': test_result['status'],
                            'error': test_result['error'],
                            'execution_time': test_result.get('execution_time'),
                            'memory_used': test_result.get('memory_used'),
                        }
                
                # 全部通过
                return {
                    'status': 'ACCEPTED',
                    'execution_time': test_result.get('execution_time'),
                    'memory_used': test_result.get('memory_used'),
                }
                
        except Exception as e:
            return {
                'status': 'RUNTIME_ERROR',
                'error': str(e)
            }
    
    def _compile_code(self, temp_dir):
        """编译Verilog代码"""
        try:
            # 写入用户代码到临时文件
            source_file = os.path.join(temp_dir, 'submission.v')
            with open(source_file, 'w') as f:
                f.write(self.code)
            
            # 编译代码
            output_file = os.path.join(temp_dir, 'submission')
            compile_cmd = ['iverilog', '-o', output_file, source_file]
            
            process = subprocess.run(
                compile_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
                text=True
            )
            
            if process.returncode != 0:
                return {
                    'success': False,
                    'error': process.stderr
                }
            
            return {'success': True}
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': '编译超时'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _run_test_case(self, temp_dir, test_case):
        """运行单个测试用例"""
        try:
            # 准备测试用例输入文件
            testbench_file = os.path.join(temp_dir, 'testbench.v')
            
            # 这里假设每个测试用例都有一个testbench.v文件
            # 实际情况下可能需要根据提交的代码动态生成testbench
            shutil.copy(test_case.testbench_file.path, testbench_file)
            
            # 编译测试用例
            output_file = os.path.join(temp_dir, 'testbench')
            compile_cmd = ['iverilog', '-o', output_file, testbench_file, os.path.join(temp_dir, 'submission.v')]
            
            process = subprocess.run(
                compile_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
                text=True
            )
            
            if process.returncode != 0:
                return {
                    'success': False,
                    'status': 'COMPILE_ERROR',
                    'error': process.stderr
                }
            
            # 运行测试
            start_time = time.time()
            run_cmd = ['vvp', output_file]
            
            process = subprocess.run(
                run_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.problem.time_limit,
                text=True
            )
            
            execution_time = (time.time() - start_time) * 1000  # 转换为毫秒
            
            # 检查输出是否符合预期
            actual_output = process.stdout.strip()
            expected_output = test_case.expected_output.strip()
            
            if actual_output != expected_output:
                return {
                    'success': False,
                    'status': 'WRONG_ANSWER',
                    'error': f'预期输出:\n{expected_output}\n\n实际输出:\n{actual_output}',
                    'execution_time': execution_time,
                    'memory_used': None  # Verilog模拟器不易获取内存使用情况
                }
            
            return {
                'success': True,
                'execution_time': execution_time,
                'memory_used': None
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'status': 'TIME_LIMIT_EXCEEDED',
                'error': f'执行超过时间限制 {self.problem.time_limit}秒'
            }
        except Exception as e:
            return {
                'success': False,
                'status': 'RUNTIME_ERROR',
                'error': str(e)
            }
