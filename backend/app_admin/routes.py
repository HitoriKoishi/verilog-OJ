from flask import Blueprint, request, jsonify
from flask_cors import CORS
from flask_login import current_user
from models import User, Problem, db, login_required, admin_required

admin_bp = Blueprint('admin', __name__)
CORS(admin_bp, resources={r"/*": {"origins": "http://localhost:5173", "supports_credentials": True}})

# 获取所有用户
@admin_bp.route('/user', methods=['GET'])
@login_required
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin
    } for user in users])

# 更新用户信息
@admin_bp.route('/user/<int:user_id>', methods=['PUT'])
@login_required
@admin_required
def update_user(user_id):
    # 检查是否是当前管理员
    if user_id == current_user.id:
        return jsonify({
            "status": "error",
            "message": "管理员不能修改自己的信息，请使用用户设置功能"
        }), 403
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    # 检查是否试图修改最后一个管理员的权限
    if 'is_admin' in data and not data['is_admin']:
        admin_count = User.query.filter_by(is_admin=True).count()
        if admin_count <= 1 and user.is_admin:
            return jsonify({
                "status": "error",
                "message": "不能移除最后一个管理员的权限"
            }), 403
    
    # 更新用户信息
    if 'username' in data:
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({
                "status": "error",
                "message": "用户名已被使用"
            }), 409
        user.username = data['username']
        
    if 'email' in data:
        # 检查邮箱是否已存在
        if data['email']:  # 只在邮箱不为空时检查
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != user_id:
                return jsonify({
                    "status": "error",
                    "message": "邮箱已被使用"
                }), 409
        user.email = data['email']
        
    if 'is_admin' in data:
        user.is_admin = data['is_admin']
        
    if 'password' in data:
        user.set_password(data['password'])
        
    try:
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "数据库更新失败"
        }), 500

# 删除用户
@admin_bp.route('/user/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    # 检查是否是当前管理员
    if user_id == current_user.id:
        return jsonify({
            "status": "error",
            "message": "管理员不能删除自己的账户"
        }), 403
    
    user = User.query.get_or_404(user_id)
    
    # 检查是否试图删除最后一个管理员
    if user.is_admin:
        admin_count = User.query.filter_by(is_admin=True).count()
        if admin_count <= 1:
            return jsonify({
                "status": "error",
                "message": "不能删除最后一个管理员账户"
            }), 403
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "删除用户失败"
        }), 500

# 获取所有题目
@admin_bp.route('/problem', methods=['GET'])
@login_required
@admin_required
def get_problems():
    problems = Problem.query.all()
    return jsonify([{
        'id': problem.id,
        'title': problem.title,
        'folder_path': problem.folder_path,
        'difficulty': problem.difficulty,
        'tags': problem.tags,
        'pre_problems': problem.pre_problems,
        'next_problems': problem.next_problems,
        'description': problem.description,
        'code_temp': problem.code_temp
    } for problem in problems])

# 更新题目信息
@admin_bp.route('/problem/<int:problem_id>', methods=['PUT'])
@login_required
@admin_required
def update_problem(problem_id):
    problem = Problem.query.get_or_404(problem_id)
    data = request.get_json()
    
    if 'title' in data:
        problem.title = data['title']
    if 'folder_path' in data:
        problem.folder_path = data['folder_path']
    if 'difficulty' in data:
        problem.difficulty = data['difficulty']
    if 'tags' in data:
        problem.tags = data['tags']
    if 'pre_problems' in data:
        problem.pre_problems = data['pre_problems']
    if 'next_problems' in data:
        problem.next_problems = data['next_problems']
    if 'description' in data:
        problem.description = data['description']
    if 'code_temp' in data:
        problem.code_temp = data['code_temp']
        
    try:
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "更新题目失败"
        }), 500

# 删除题目
@admin_bp.route('/problem/<int:problem_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_problem(problem_id):
    problem = Problem.query.get_or_404(problem_id)
    try:
        db.session.delete(problem)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "删除题目失败"
        }), 500 