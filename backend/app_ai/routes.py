"""
提供AI分析相关的API路由
"""

from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from flask_cors import CORS
from models import Problem, Submission, User, SubmissionStatus
from exts import db
import os
from pathlib import Path
from models import BASE_DIR, PROB_DIR

from .deepseek_api import deepseek_api

ai_bp = Blueprint('ai', __name__)
CORS(ai_bp, resources={r"/*": {"origins": "http://localhost:5173", "supports_credentials": True}})

@ai_bp.route('/analyze/<int:submission_id>', methods=['GET'])
@login_required
def analyze_submission(submission_id):
    """
    分析提交的代码并返回AI反馈
    
    参数:
    - submission_id: 提交ID
    
    返回:
    - JSON格式的AI分析结果
    """
    try:
        # 获取提交记录
        submission = Submission.query.get(submission_id)
        if not submission:
            return jsonify({"error": "提交记录不存在"}), 404
            
        # 检查权限（只能查看自己的提交，除非是管理员）
        if submission.user_id != current_user.id and not current_user.is_admin:
            return jsonify({"error": "无权访问此提交记录"}), 403
            
        # 验证提交状态（必须是失败状态才提供分析）
        if submission.status != SubmissionStatus.FAILED:
            return jsonify({"error": "只能分析失败的提交"}), 400
            
        # 获取题目信息
        problem = Problem.query.get(submission.problem_id)
        if not problem:
            return jsonify({"error": "题目不存在"}), 404
            
        # 获取相关文件内容
        problem_id = problem.id
        problem_title = problem.title
        problem_description = problem.description
        
        # 获取测试台代码
        testbench_path = PROB_DIR / f"exp{problem_id}" / "project" / "test_bench.v"
        # 获取参考实现代码
        reference_path = PROB_DIR / f"exp{problem_id}" / "project" / "ref_module.v"
        
        # 读取文件内容
        testbench_code = ""
        reference_code = ""
        log_content = ""
        waveform_content = ""
        
        try:
            with open(testbench_path, 'r', encoding='utf-8') as f:
                testbench_code = f.read()
        except Exception as e:
            print(f"读取测试台代码失败: {e}")
            testbench_code = "无法读取测试台代码"
            
        try:
            with open(reference_path, 'r', encoding='utf-8') as f:
                reference_code = f.read()
        except Exception as e:
            print(f"读取参考代码失败: {e}")
            reference_code = "无法读取参考代码"
            
        # 获取日志内容
        if submission.log_path and os.path.exists(BASE_DIR / submission.log_path):
            try:
                with open(BASE_DIR / submission.log_path, 'r', encoding='utf-8') as f:
                    log_content = f.read()
            except Exception as e:
                print(f"读取日志失败: {e}")
                log_content = "无法读取日志"
        else:
            log_content = "日志文件不存在"
            
        # 获取波形内容（可选）
        if submission.waveform_path and os.path.exists(BASE_DIR / submission.waveform_path):
            try:
                with open(BASE_DIR / submission.waveform_path, 'r', encoding='utf-8') as f:
                    waveform_content = f.read()
            except Exception as e:
                print(f"读取波形失败: {e}")
                waveform_content = "无法读取波形"
        else:
            waveform_content = "波形文件不存在"
            
        # 调用AI分析
        analysis_result = deepseek_api.analyze_code(
            problem_title=problem_title,
            problem_description=problem_description,
            testbench_code=testbench_code,
            reference_code=reference_code,
            user_code=submission.code,
            log_content=log_content,
            waveform=waveform_content,
            error_code=submission.error_code
        )
        
        # 返回分析结果
        return jsonify({
            "success": True,
            "analysis": analysis_result
        })
        
    except Exception as e:
        print(f"AI分析过程中出错: {e}")
        return jsonify({"error": f"分析过程中发生错误: {str(e)}"}), 500 