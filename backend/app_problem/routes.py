from flask import Blueprint, request, jsonify, url_for, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, UserCode, Problem, Submission, SubmissionStatus, login_required
from datetime import datetime
from exts import db
from app_submit.run_sim import simulation_queue
import re
import os
from pathlib import Path
from flask import current_app, abort

problem_bp = Blueprint('problem', __name__)
CORS(problem_bp, resources={r"/*": {"origins": "http://localhost:5173", "supports_credentials": True}})


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
    # 将 submission_id 加入队列
    print(f"将提交ID {submission.id} 加入仿真队列")
    simulation_queue.put(submission.id)
    print(f"仿真队列大小: {simulation_queue.qsize()}")
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
    # 获取文档内容
    doc_content = problem.description
    # 替换相对路径为绝对路径
    def replace_relative_paths(match):
        captured_path = match.group(2)  # 获取括号内捕获的完整路径
        # 提取路径中的文件名部分
        relative_path = os.path.basename(captured_path)
        
        # 只处理没有完整URL的相对路径 (现在relative_path应该是纯文件名)
        if not relative_path.startswith(('http://', 'https://', '/')):
            # 使用提取的文件名构建URL
            absolute_url = url_for('problem.serve_prob_static', filename=f'exp{id}/doc/{relative_path}', _external=True)
            # print(f"[Problem ID: {id}] 修正后生成图片URL: {absolute_url} (原始捕获: {captured_path}, 提取文件名: {relative_path})")
            return f'![{match.group(1)}]({absolute_url})'
        # print(f"[Problem ID: {id}] 保持原始URL/路径: {captured_path}")
        return match.group(0)
    
    # 修正正则表达式，使用 r'!\\[(.*?)\\]\\((.*?)\\)' 来匹配 ![alt](path)
    doc_content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_relative_paths, doc_content)
    # 检查用户是否完成解答，仅在用户登录时检查
    is_completed = get_completion_status(user_id, id) if user_id else None
    # 构建响应数据
    response_data = {
        "id": problem.id,
        "title": problem.title,
        "document": doc_content,
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

# ---------- 获取用户对特定问题的提交记录 ----------
@problem_bp.route('/<int:id>/submit_history', methods=['GET'])
@login_required
def getSubmissionHistory(id):
    """获取用户对特定问题的提交记录"""
    user_id = current_user.id
    
    # 验证用户和问题是否存在
    if not (User.query.get(user_id)) or not (Problem.query.get(id)):
        return jsonify({"error": "用户或问题不存在"}), 404
    
    # 查询该用户对特定问题的所有提交记录
    submissions = Submission.query.filter_by(
        user_id=user_id,
        problem_id=id
    ).order_by(Submission.created_at.desc()).all()
    
    # 构建响应数据结构
    submission_history = []
    for submission in submissions:
        submission_history.append({
            "submission_id": submission.id,
            "created_at": submission.created_at,
            "status": submission.status
        })
    
    return jsonify(submission_history)

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


@problem_bp.route('/static/Prob/<path:filename>')
def serve_prob_static(filename):
    """提供 Prob 文件夹中的静态资源"""
    # print(f"请求静态资源：{filename}")
    # 构建完整路径
    full_path = os.path.join('Prob', filename)
    if os.path.exists(full_path):
        return send_from_directory('Prob', filename)
    
    # 如果文件不存在，尝试在同一目录下查找其他图片文件
    dir_path = os.path.dirname(full_path)
    if os.path.exists(dir_path):
        # 如果是example.png请求，查看目录中是否有其他图片
        if 'example.png' in filename:
            for img_ext in ['.png', '.jpg', '.jpeg', '.gif']:
                # 尝试pic1.png等常见名称
                for img_name in ['pic1', 'pic']:
                    alt_name = filename.replace('example.png', f'{img_name}{img_ext}')
                    alt_path = os.path.join('Prob', alt_name)
                    if os.path.exists(alt_path):
                        # print(f"找到替代文件：{alt_name}")
                        return send_from_directory('Prob', alt_name)
    
    # 如果没有找到任何替代文件，返回404
    print(f"文件未找到，返回 404: {full_path}") # 添加日志
    abort(404)