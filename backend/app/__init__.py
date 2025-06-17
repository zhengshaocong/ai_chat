from flask import Flask
from flask_cors import CORS
from config.database import engine
from app.models.models import Base
import os

def create_app():
    app = Flask(__name__)
    # 配置 CORS，允许所有来源
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # 配置密钥
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

    # 创建数据库表
    Base.metadata.create_all(bind=engine)

    # 注册蓝图
    from app.controllers.ai_app_controller import ai_app_bp
    from app.controllers.chat_controller import chat_bp
    from app.controllers.auth_controller import auth_bp

    app.register_blueprint(ai_app_bp, url_prefix='/ai-apps')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app 