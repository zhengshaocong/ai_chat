from app.models.models import User
from config.database import SessionLocal
from datetime import datetime, timedelta
import jwt
from flask import current_app
import traceback

class AuthService:
    @staticmethod
    def register(username, password):
        db = SessionLocal()
        try:
            # 检查用户名是否已存在
            if db.query(User).filter_by(username=username).first():
                print('用户名已存在')
                return False, "用户名已存在"
            
            # 创建新用户
            user = User(username=username)
            user.set_password(password)  # 使用 set_password 方法加密密码
            
            db.add(user)
            db.commit()
            return True, "注册成功"
        except Exception as e:
            db.rollback()
            print('注册异常:', str(e))
            traceback.print_exc()
            return False, f"注册失败: {str(e)}"
        finally:
            db.close()

    @staticmethod
    def login(username, password):
        db = SessionLocal()
        try:
            user = db.query(User).filter_by(username=username).first()
            
            if not user or not user.check_password(password):
                return False, "用户名或密码错误"
            
            if not user.is_active:
                return False, "账号已被禁用"
            
            # 生成 JWT token
            token = jwt.encode(
                {
                    'user_id': user.id,
                    'username': user.username,
                    'exp': datetime.utcnow() + timedelta(days=1)
                },
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            
            return True, {
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username
                }
            }
        finally:
            db.close()

    @staticmethod
    def get_user_by_id(user_id):
        db = SessionLocal()
        try:
            return db.query(User).get(user_id)
        finally:
            db.close() 