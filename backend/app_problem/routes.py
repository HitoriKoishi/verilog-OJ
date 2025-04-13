from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, UserCode, Problem, Submission, SubmissionStatus
from datetime import datetime
from exts import db

problem_bp = Blueprint('problem', __name__)


# ---------- 保存用户代码草稿 ----------
@problem_bp.route('/<int:id>/save', methods=['POST'])
@login_required
def saveDraft(id):
    """保存代码草稿"""
    user_id = current_user.id
    code = request.get_json().get('code')
    # 验证存在性
    if not (User.query.get(user_id)) or not (Problem.query.get(id)):
        return jsonify({"error": "用户或问题不存在"}), 404
    # 更新或创建暂存记录
    draft = UserCode.query.filter_by(
        user_id=user_id,
        problem_id=id
    ).first()
    if draft:
        draft.draft_code = code
        draft.updated_at = datetime.now()
    else:
        draft = UserCode(
            user_id=user_id,
            problem_id=id,
            draft_code=code,
            updated_at=datetime.now()
        )
        db.session.add(draft)
    db.session.commit()
    return jsonify({"status": "success"})


# ---------- 获取用户代码草稿 ----------
@problem_bp.route('/<int:id>/load', methods=['GET'])
@login_required
def loadDraft(id):
    """取用户代码草稿"""
    user_id = current_user.id
    # 验证存在性
    if not (User.query.get(user_id)) or not (Problem.query.get(id)):
        return jsonify({"error": "用户或问题不存在"}), 404
    draft = UserCode.query.filter_by(
        user_id=user_id,
        problem_id=id
    ).first()
    if draft:
        draft_code = draft.draft_code
        draft_time = draft.updated_at
        return jsonify({
            "status": "success",
            "draft_code": draft_code,
            "draft_time": draft_time
        })
    else:
        return jsonify({
            "status": "failed"
        })


# ---------- 提交代码，创建提交ID ----------
@problem_bp.route('/<int:id>/submit', methods=['POST'])
@login_required
def submitSolution(id):
    """提交代码"""
    user_id = current_user.id
    code = request.get_json().get('code')
    # 验证存在性
    if not (User.query.get(user_id)) or not (Problem.query.get(id)):
        return jsonify({"error": "用户或问题不存在"}), 404
    # 创建提交记录
    submission = Submission(
        user_id=user_id,
        problem_id=id,
        code=code,
        status=SubmissionStatus.QUEUED,  # 初始状态为排队中
        created_at=datetime.now()
    )
    db.session.add(submission)
    db.session.commit()
    return jsonify({
        "status": "success",
        "submission_id": submission.id
        })


# ---------- 获取Prob列表 ----------
@problem_bp.route('/', methods=['GET'])
def getProblems():
    """获取问题列表，返回ID、标题、难度、标签以及用户是否完成解答（仅登录用户可见）"""
    user_id = current_user.id if current_user.is_authenticated else None
    problems = Problem.query.all()
    # 构建响应数据结构
    problems_list = []
    for p in problems:
        # 获取提交用户数和通过用户数
        stats = get_problem_statistics(p.id)
        # 检查用户是否完成解答，仅在用户登录时检查
        is_completed = get_completion_status(user_id, p.id) if user_id else None
        problems_list.append({
            "id": p.id,
            "title": p.title,
            "difficulty": p.difficulty,
            "tags": p.tags.split(',') if p.tags else [],
            "submitted_users_count": stats["submitted_users_count"],  # 提交用户数
            "passed_users_count": stats["passed_users_count"],        # 通过用户数
            **({"is_completed": is_completed} if user_id else {})  # 动态添加字段
        })
    return jsonify(problems_list)


# ---------- 获取单个Prob详情 ----------
@problem_bp.route('/<int:id>', methods=['GET'])
def getProblem(id):
    """获取单个问题详情，返回ID、标题、文档、难度、标签、代码模板以及用户是否完成解答（仅登录用户可见）"""
    user_id = current_user.id if current_user.is_authenticated else None
    problem = Problem.query.get(id)
    if not problem:
        return jsonify({"error": "Problem not found"}), 404
    # 检查用户是否完成解答，仅在用户登录时检查
    is_completed = get_completion_status(user_id, id) if user_id else None
    # 构建响应数据
    response_data = {
        "id": problem.id,
        "title": problem.title,
        "document": problem.description,
        "difficulty": problem.difficulty,
        "tags": problem.tags.split(',') if problem.tags else [],
        "code_template": problem.code_temp,
        **({"is_completed": is_completed} if user_id else {})  # 动态添加字段
    }
    return jsonify(response_data)

# ---------- 获取用户对各个问题的完成状态 ----------
@problem_bp.route('/status', methods=['GET'])
@login_required
def getUserCompletionStatus():
    """获取用户对各个问题的完成状态，仅返回问题ID和完成状态"""
    user_id = current_user.id
    # 验证存在性
    if not User.query.get(user_id):
        return jsonify({"error": "用户不存在"}), 404
    problems = Problem.query.all()
    # 构建响应数据结构
    completion_status_list = []
    for p in problems:
        is_completed = get_completion_status(user_id, p.id)
        completion_status_list.append({
            "id": p.id,
            "completion_status": is_completed
        })
    return jsonify(completion_status_list)

def get_completion_status(user_id, problem_id):
    """
    获取用户对某个问题的完成状态。
    :param user_id: 用户ID
    :param problem_id: 问题ID
    :return: 完成状态字符串（"已完成"、"失败"、"运行中"、"未完成"）
    """
    success_submission = Submission.query.filter_by(
        user_id=user_id,
        problem_id=problem_id,
        status=SubmissionStatus.SUCCESS
    ).first()
    if success_submission:
        return "已完成"
    latest_submission = Submission.query.filter_by(
        user_id=user_id,
        problem_id=problem_id
    ).order_by(Submission.created_at.desc()).first()
    if latest_submission:
        if latest_submission.status == SubmissionStatus.FAILED:
            return "失败"
        elif latest_submission.status in [SubmissionStatus.QUEUED, SubmissionStatus.RUNNING]:
            return "运行中"
    return "未完成"

def get_problem_statistics(problem_id):
    """
    获取某个问题的统计信息。
    :param problem_id: 问题ID
    :return: 一个字典，包含提交用户数和通过用户数
    """
    # 获取提交了该问题的用户数（去重）
    submitted_users_count = db.session.query(Submission.user_id).filter_by(
        problem_id=problem_id
    ).distinct().count()

    # 获取通过了该问题的用户数（去重）
    passed_users_count = db.session.query(Submission.user_id).filter_by(
        problem_id=problem_id,
        status=SubmissionStatus.SUCCESS
    ).distinct().count()

    return {
        "submitted_users_count": submitted_users_count,
        "passed_users_count": passed_users_count
    }

