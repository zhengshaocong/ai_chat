from app import create_app
from app.models.models import AIApp, ChatSession, ChatSessionDetail, User
from config import SessionLocal, Base, engine

def init_db():
    # 删除所有现有表
    Base.metadata.drop_all(bind=engine)
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    app = create_app()
    with app.app_context():
        db = SessionLocal()
        
        # 创建示例用户
        test_user = User(
            username="test",
            email="test@example.com"
        )
        test_user.set_password("test123")  # 使用set_password方法设置密码
        db.add(test_user)
        db.commit()
        
        # 创建示例AI应用
        ai_apps = [
            AIApp(
                name="数据分析助手",
                description="帮助您分析数据，生成图表和报告",
                icon="https://example.com/data-analysis.png"
            ),
            AIApp(
                name="协作能手",
                description="协助团队协作，管理任务和项目",
                icon="https://example.com/collaboration.png"
            ),
            AIApp(
                name="数学答题助手",
                description="解答数学问题，提供详细的解题步骤",
                icon="https://example.com/math.png"
            )
        ]
        
        for app in ai_apps:
            db.add(app)
        db.commit()
        
        # 为每个AI应用创建示例会话
        for app in ai_apps:
            session = ChatSession(
                ai_app_id=app.id,
                title="示例会话"
            )
            db.add(session)
            db.commit()
            
            # 添加示例消息
            messages = [
                ChatSessionDetail(
                    chat_session_id=session.id,
                    role="user",
                    content="你好，请帮我分析一下这组数据。"
                ),
                ChatSessionDetail(
                    chat_session_id=session.id,
                    role="assistant",
                    content="好的，我很乐意帮您分析数据。请提供您想要分析的数据。"
                )
            ]
            
            for message in messages:
                db.add(message)
            db.commit()
        
        db.close()

if __name__ == "__main__":
    init_db() 