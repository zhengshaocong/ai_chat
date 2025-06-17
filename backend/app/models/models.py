from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base
from werkzeug.security import generate_password_hash, check_password_hash

class AIApp(Base):
    __tablename__ = "ai_apps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    chat_sessions = relationship("ChatSession", back_populates="ai_app")

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    ai_app_id = Column(Integer, ForeignKey("ai_apps.id"))
    title = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ai_app = relationship("AIApp", back_populates="chat_sessions")
    messages = relationship("ChatSessionDetail", back_populates="chat_session")
    files = relationship("ChatFile", back_populates="chat_session")

class ChatSessionDetail(Base):
    __tablename__ = "chat_session_details"

    id = Column(Integer, primary_key=True, index=True)
    chat_session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    role = Column(String(20))  # 'user' or 'assistant'
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat_session = relationship("ChatSession", back_populates="messages")

class ChatFile(Base):
    __tablename__ = "chat_files"

    id = Column(Integer, primary_key=True, index=True)
    chat_session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    file_name = Column(String(255))
    file_path = Column(String(255))
    file_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    chat_session = relationship("ChatSession", back_populates="files")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 