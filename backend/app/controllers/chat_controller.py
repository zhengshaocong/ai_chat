from flask import Blueprint, jsonify, request
from app.services.chat_service import ChatService
from config import get_db

chat_bp = Blueprint('chat', __name__)
chat_service = ChatService()

@chat_bp.route('/sessions/<int:app_id>', methods=['GET'])
def get_chat_sessions(app_id):
    db = next(get_db())
    sessions = chat_service.get_chat_sessions(db, app_id)
    return jsonify([{
        'id': session.id,
        'title': session.title,
        'created_at': session.created_at.isoformat(),
        'updated_at': session.updated_at.isoformat()
    } for session in sessions])

@chat_bp.route('/sessions', methods=['POST'])
def create_chat_session():
    db = next(get_db())
    data = request.json
    session = chat_service.create_chat_session(db, data['ai_app_id'], data['title'])
    return jsonify({
        'id': session.id,
        'title': session.title,
        'created_at': session.created_at.isoformat()
    })

@chat_bp.route('/sessions/<int:session_id>', methods=['DELETE'])
def delete_chat_session(session_id):
    db = next(get_db())
    chat_service.delete_chat_session(db, session_id)
    return jsonify({'message': '会话已删除'})

@chat_bp.route('/messages/<int:session_id>', methods=['GET'])
def get_chat_messages(session_id):
    db = next(get_db())
    messages = chat_service.get_chat_messages(db, session_id)
    return jsonify([{
        'id': msg.id,
        'role': msg.role,
        'content': msg.content,
        'created_at': msg.created_at.isoformat()
    } for msg in messages])

@chat_bp.route('/messages', methods=['POST'])
def create_chat_message():
    db = next(get_db())
    data = request.json
    message = chat_service.create_chat_message(
        db,
        data['session_id'],
        data['role'],
        data['content']
    )
    return jsonify({
        'id': message.id,
        'role': message.role,
        'content': message.content,
        'created_at': message.created_at.isoformat()
    }) 