from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import User, UserCode, Problem, Submission, SubmissionStatus, ErrorCode, SimulationResult
from threading import Lock
from exts import db
from run_sim import sim_run_verilog as sim_run_verilog

submit_bp = Blueprint('submissions', __name__)

simulation_lock = Lock()

# ---------- 获取用户历史提交记录 ----------
@submit_bp.route('/all', methods=['GET'])
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
        "subid": sub.id,
        "date": sub.created_at.isoformat(),
        "status": sub.status
    } for sub in submissions])

# ---------- 获取提交结果，运行仿真 ----------
@submit_bp.route('/<int:submission_id>', methods=['GET'])
def getSubmission(submission_id):
    """触发仿真执行并返回结果"""
    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({"error": "提交记录不存在"}), 404
    # 最终状态直接返回
    if submission.status in [SubmissionStatus.SUCCESS, SubmissionStatus.FAILED]:
        return _format_response(submission)
    # 加锁防止并发执行
    with simulation_lock:
        # 刷新对象状态
        submission = Submission.query.get(submission_id)
        if submission.status != SubmissionStatus.QUEUED:
            return _format_response(submission)
        try:
            # 更新为运行状态
            submission.status = SubmissionStatus.RUNNING
            db.session.commit()
            # 执行仿真
            sim_result = sim_run_verilog(submission_id)
            # 更新数据库记录
            submission.status = SubmissionStatus.SUCCESS if sim_result.error_code == ErrorCode.SUCCESS else SubmissionStatus.FAILED
            submission.error_code = sim_result.error_code.name
            submission.log_path = sim_result.log_path
            submission.waveform_path = sim_result.waveform_path
        except Exception as e:
            # 错误处理
            submission.status = SubmissionStatus.FAILED
            submission.error_code = str(e)
            submission.log_path = ""
            submission.waveform_path = ""
        finally:
            db.session.commit()
    return _format_response(submission)

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
