from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user
from flask_cors import CORS
from models import User, UserCode, Problem, Submission, SubmissionStatus, ErrorCode, SimulationResult, login_required
from threading import Lock
from exts import db
import os
from app_submit.run_sim import sim_run_verilog

submit_bp = Blueprint('submission', __name__)
CORS(submit_bp, resources={r"/*": {"origins": "http://localhost:5173", "supports_credentials": True}})

simulation_lock = Lock()

# ---------- 获取用户历史提交记录 ----------
@submit_bp.route('/', methods=['GET'])
@login_required
def getUserSubmissions():
    """获取提交历史，返回用户的历史提交ID，status，日期"""
    user_id = current_user.id
    # 验证存在性
    if not User.query.get(user_id):
        return jsonify({"error": "用户不存在"}), 404
    # 查询提交记录（仅获取必要字段）
    submissions = Submission.query.with_entities(
        Submission.id,
        Submission.created_at,
        Submission.status
    ).filter_by(user_id=user_id).order_by(Submission.created_at.desc()).all()
    # 构建响应数据
    return jsonify([{
        "submission_id": sub.id,
        "created_at": sub.created_at.isoformat(),
        "status": sub.status
    } for sub in submissions])


# ---------- 获取提交结果，运行仿真 ----------
@submit_bp.route('/<int:submission_id>', methods=['GET'])
def getSubmission(submission_id):
    """获取仿真结果"""
    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({"error": "提交记录不存在"}), 404
    # 返回仿真结果
    return _format_response(submission)


# ---------- 获取日志文件内容 ----------
@submit_bp.route('/<int:submission_id>/log', methods=['GET'])
def getLog(submission_id):
    """获取指定提交的日志文件内容"""
    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({"error": "提交记录不存在"}), 404
    log_path = submission.log_path
    if not log_path or not os.path.exists(log_path):
        return jsonify({"error": "日志文件不存在"}), 404
    try:
        # 读取日志文件内容
        with open(log_path, 'r', encoding='utf-8') as f:
            log_content = f.read()
        return jsonify({"status": "success", "log_content": log_content})
    except Exception as e:
        return jsonify({"error": f"无法读取日志文件: {str(e)}"}), 500


# ---------- 获取波形文件内容 ----------
@submit_bp.route('/<int:submission_id>/waveform', methods=['GET'])
def getWaveform(submission_id):
    """获取指定提交的波形文件内容"""
    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({"error": "提交记录不存在"}), 404
    waveform_path = submission.waveform_path
    if not waveform_path or not os.path.exists(waveform_path):
        return jsonify({"error": "波形文件不存在"}), 404
    try:
        # 读取波形文件内容
        with open(waveform_path, 'r', encoding='utf-8') as f:
            waveform_content = f.read()
        return jsonify({"status": "success", "waveform_content": waveform_content})
    except Exception as e:
        return jsonify({"error": f"无法读取波形文件: {str(e)}"}), 500


def _format_response(submission):
    """统一响应格式化"""
    response_data = {
        "problem_id": submission.problem_id,
        "status": submission.status,
        "error_code": submission.error_code,
        "log_path": submission.log_path,
        "waveform_path": submission.waveform_path,
        "created_at": submission.created_at.isoformat()
    }
    return jsonify(response_data)
