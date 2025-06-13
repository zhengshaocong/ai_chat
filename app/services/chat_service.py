from app.models.models import ChatSession, ChatSessionDetail, ChatFile
from datetime import datetime

class ChatService:
    def get_chat_sessions(self, db, app_id):
        return db.query(ChatSession).filter(ChatSession.ai_app_id == app_id).all()

    def create_chat_session(self, db, ai_app_id, title):
        session = ChatSession(
            ai_app_id=ai_app_id,
            title=title[:50] if title else "新会话"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    def delete_chat_session(self, db, session_id):
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            db.delete(session)
            db.commit()

    def get_chat_messages(self, db, session_id):
        return db.query(ChatSessionDetail).filter(
            ChatSessionDetail.chat_session_id == session_id
        ).order_by(ChatSessionDetail.created_at).all()

    def create_chat_message(self, db, session_id, role, content):
        message = ChatSessionDetail(
            chat_session_id=session_id,
            role=role,
            content=content
        )
        db.add(message)
        
        # 更新会话的更新时间
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            session.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(message)
        return message

    def save_chat_file(self, db, session_id, file_name, file_path, file_type):
        chat_file = ChatFile(
            chat_session_id=session_id,
            file_name=file_name,
            file_path=file_path,
            file_type=file_type
        )
        db.add(chat_file)
        db.commit()
        db.refresh(chat_file)
        return chat_file 