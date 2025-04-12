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
    return jsonify({"submission_id": submission.id})



# ---------- 获取Prob列表 ----------
@problem_bp.route('/', methods=['GET'])
def getProblems():
    """获取问题列表，返回ID、标题、难度和标签"""
    problems = Problem.query.all()
    # 构建响应数据结构
    problems_list = [{
            "id": p.id,
            "title": p.title,
            "difficulty": p.difficulty,
            "tags": p.tags.split(',') if p.tags else []  # 将字符串转换为数组
        }for p in problems]
    return jsonify(problems_list)


# ---------- 获取单个Prob详情 ----------
@problem_bp.route('/<int:id>', methods=['GET'])
def getProblem(id):
    """获取单个问题详情，返回ID、标题、文档、难度、标签、代码模板"""
    problem = Problem.query.get(id)
    if not problem:
        return jsonify({"error": "Problem not found"}), 404
    # 构建响应数据
    response_data = {
        "id": problem.id,
        "title": problem.title,
        "document": problem.description,  # 完整文档内容
        "difficulty": problem.difficulty,
        "tags": problem.tags.split(',') if problem.tags else [],  # 转换为数组
        "code_template": problem.code_temp  # 代码编辑器初始内容
    }
    return jsonify(response_data)

