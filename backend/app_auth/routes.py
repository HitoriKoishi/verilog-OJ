from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, login_required
from exts import db

user_bp = Blueprint('user', __name__)
CORS(user_bp, resources={r"/*": {"origins": "http://localhost:5173", "supports_credentials": True}})


# ---------- 登录路由 ----------
@user_bp.route('/login', methods=['POST'])
def loginUser():
    username = request.get_json().get('username')
    password = request.get_json().get('password')
    if not username or not password:
        return jsonify({"status": "error", "msg": "需要用户名和密码"}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"status": "error", "msg": "用户名或密码错误"}), 401
    login_user(user)
    return jsonify({
        "status": "success",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    })

# ---------- 注销路由 ----------
@user_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logoutUser():
    logout_user()
    session.clear()  # 清除所有会话数据
    return jsonify({"status": "success"})

# ---------- 登录状态检查 ----------
@user_bp.route('/check_auth', methods=['GET'])
def checkAuth():
    if current_user.is_authenticated:
        return jsonify({
            "is_login": True,
            "user": {
                "id": current_user.id,
                "username": current_user.username
            }
        })
    return jsonify({"is_login": False})

# ---------- 注册路由 ----------
@user_bp.route('/register', methods=['POST'])
def registerUser():
    """注册接口，支持密码和邮箱"""
    username = request.get_json().get('username')
    password = request.get_json().get('password')
    email = request.get_json().get('email')
    # 验证存在性
    if not username or not password:
        return jsonify({"error": "用户名和密码为必填项"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "用户名已存在"}), 409
    if email and User.query.filter_by(email=email).first():
        return jsonify({"error": "邮箱已被注册"}), 409
    # 创建用户
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)    # 自动登录
    return jsonify({
        "status": "success",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    })

# ---------- 获取用户资料 ----------
@user_bp.route('/profile', methods=['GET'])
@login_required
def getUserProfile():
    """获取当前登录用户的详细信息"""
    user = User.query.get(current_user.id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })

# ---------- 更新用户名 ----------
@user_bp.route('/update_username', methods=['POST'])
@login_required
def updateUsername():
    """更新用户名"""
    new_username = request.get_json().get('newUsername')
    
    if not new_username:
        return jsonify({"error": "新用户名不能为空"}), 400
    
    # 检查用户名是否已存在
    if User.query.filter(User.username == new_username, User.id != current_user.id).first():
        return jsonify({"error": "该用户名已被使用"}), 409
    
    user = User.query.get(current_user.id)
    user.username = new_username
    db.session.commit()
    
    return jsonify({"status": "success", "username": new_username})

# ---------- 更新密码 ----------
@user_bp.route('/update_password', methods=['POST'])
@login_required
def updatePassword():
    """更新用户密码"""
    data = request.get_json()
    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')
    
    if not current_password or not new_password:
        return jsonify({"error": "当前密码和新密码不能为空"}), 400
    
    user = User.query.get(current_user.id)
    
    # 验证当前密码
    if not user.check_password(current_password):
        return jsonify({"error": "当前密码不正确"}), 401
    
    # 更新密码
    user.set_password(new_password)
    db.session.commit()
    
    return jsonify({"status": "success"})