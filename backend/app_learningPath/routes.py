from flask import Blueprint, jsonify, request
from models import Problem, login_required, admin_required
from app_learningPath.learningPath import get_learning_path, get_all_learning_paths, add_learning_path
from flask_login import current_user

# 创建Blueprint
learningPath_bp = Blueprint('learningPath', __name__)

@learningPath_bp.route('/all', methods=['GET'])
def get_paths():
    """获取所有学习路径"""
    paths = get_all_learning_paths()
    return jsonify(paths)

@learningPath_bp.route('/<int:path_id>', methods=['GET'])
def get_path(path_id):
    """获取单个学习路径详情"""
    path = get_learning_path(path_id)
    if not path:
        return jsonify({"error": "学习路径不存在"}), 404
    return jsonify(path)

@learningPath_bp.route('/<int:path_id>/chain', methods=['GET'])
def get_path_chain(path_id):
    """获取学习路径的完整题目链条"""
    path = get_learning_path(path_id)
    if not path:
        return jsonify({"error": "学习路径不存在"}), 404
    
    # 获取起始题目ID
    start_problem_id = path["start_problem_id"]
    
    # 构建题目链条
    chain = []
    current_id = start_problem_id
    
    # 防止循环依赖导致的无限循环
    visited_ids = set()
    
    while current_id and current_id not in visited_ids:
        # 获取当前题目
        problem = Problem.query.get(current_id)
        if not problem:
            break
        
        # 标记为已访问
        visited_ids.add(current_id)
        
        # 添加到链条
        chain.append({
            "id": problem.id,
            "title": problem.title,
            "difficulty": problem.difficulty,
            "tags": problem.tags.replace('，', ',').split(',') if problem.tags else []
        })
        
        # 获取下一个题目ID
        next_ids = [int(x.strip()) for x in problem.next_problems.replace('，', ',').split(',') 
                   if x.strip()] if problem.next_problems else []
        
        # 如果有多个后置题目，选择第一个
        current_id = next_ids[0] if next_ids else None
    
    return jsonify({
        "path_id": path_id,
        "path_name": path["name"],
        "path_description": path["description"],
        "problems_chain": chain
    })

# 管理员路由 - 添加学习路径
@learningPath_bp.route('/add', methods=['POST'])
@login_required
@admin_required
def add_path():
    """添加新的学习路径（仅管理员）"""
    # 检查是否为管理员
    if not current_user.is_admin:
        return jsonify({"error": "权限不足"}), 403
    
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    start_problem_id = data.get('start_problem_id')
    
    # 验证数据
    if not all([name, description, start_problem_id]):
        return jsonify({"error": "缺少必要参数"}), 400
    
    # 验证起始题目是否存在
    if not Problem.query.get(start_problem_id):
        return jsonify({"error": "起始题目不存在"}), 404
    
    # 添加学习路径
    path_id = add_learning_path(name, description, start_problem_id)
    return jsonify({
        "status": "success",
        "path_id": path_id
    })