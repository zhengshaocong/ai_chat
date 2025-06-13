from flask import Flask
from flask_cors import CORS
from config.database import engine
from app.models.models import Base

def create_app():
    app = Flask(__name__)
    CORS(app)

    # 创建数据库表
    Base.metadata.create_all(bind=engine)

    # 注册蓝图
    from app.controllers.ai_app_controller import ai_app_bp
    from app.controllers.chat_controller import chat_bp

    app.register_blueprint(ai_app_bp, url_prefix='/api/ai-apps')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')

    return app 