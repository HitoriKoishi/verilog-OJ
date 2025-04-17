import click
from flask.cli import FlaskGroup
from app import app
from models import User, db

cli = FlaskGroup(app)

@cli.command('create-admin')
@click.argument('username')
@click.argument('password')
@click.option('--email', default=None, help='管理员邮箱')
def create_admin(username, password, email):
    """创建管理员账户"""
    with app.app_context():
        if User.query.filter_by(username=username).first():
            click.echo(f'错误：用户名 {username} 已存在')
            return

        if email and User.query.filter_by(email=email).first():
            click.echo(f'错误：邮箱 {email} 已被使用')
            return

        user = User(username=username, email=email, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f'成功创建管理员账户 {username}')

@cli.command('list-admins')
def list_admins():
    """列出所有管理员账户"""
    with app.app_context():
        admins = User.query.filter_by(is_admin=True).all()
        if not admins:
            click.echo('当前没有管理员账户')
            return
        
        click.echo('管理员列表：')
        for admin in admins:
            click.echo(f'ID: {admin.id}, 用户名: {admin.username}, 邮箱: {admin.email or "无"}')

@cli.command('set-admin')
@click.argument('username')
def set_admin(username):
    """将现有用户设置为管理员"""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            click.echo(f'错误：用户 {username} 不存在')
            return
        
        if user.is_admin:
            click.echo(f'用户 {username} 已经是管理员')
            return
        
        user.is_admin = True
        db.session.commit()
        click.echo(f'已将用户 {username} 设置为管理员')

@cli.command('remove-admin')
@click.argument('username')
def remove_admin(username):
    """移除管理员权限"""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            click.echo(f'错误：用户 {username} 不存在')
            return
        
        if not user.is_admin:
            click.echo(f'用户 {username} 不是管理员')
            return
        
        # 检查是否是最后一个管理员
        admin_count = User.query.filter_by(is_admin=True).count()
        if admin_count <= 1:
            click.echo('错误：不能移除最后一个管理员')
            return
        
        user.is_admin = False
        db.session.commit()
        click.echo(f'已移除 {username} 的管理员权限')

if __name__ == '__main__':
    cli() 