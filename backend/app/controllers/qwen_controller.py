from flask import Blueprint, jsonify, request
from app.services.qwen_service import QwenService
from config.database import get_db

qwen_bp = Blueprint('qwen', __name__)
qwen_service = QwenService()

@qwen_bp.route('/chat', methods=['POST'])
def chat_with_qwen():
    """
    与千问进行对话
    
    请求体:
    {
        "message": "用户消息",
        "session_id": 123,
        "history": [] // 可选，对话历史
    }
    """
    try:
        data = request.json
        message = data.get('message')
        session_id = data.get('session_id')
        history = data.get('history', [])
        
        if not message:
            return jsonify({'error': '消息不能为空'}), 400
        
        if not session_id:
            return jsonify({'error': '会话ID不能为空'}), 400
        
        # 调用千问服务
        result = qwen_service.chat_with_qwen(message, session_id, history)
        
        if not result['success']:
            return jsonify({'error': result['error']}), 500
        
        return jsonify({
            'success': True,
            'message': result['message'],
            'model_used': result['model_used'],
            'user_message_id': result['user_message_id'],
            'ai_message_id': result['ai_message_id']
        })
        
    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@qwen_bp.route('/models', methods=['GET'])
def get_qwen_models():
    """
    获取可用的千问模型列表
    """
    try:
        models = qwen_service.get_available_models()
        return jsonify({
            'success': True,
            'models': models
        })
        
    except Exception as e:
        return jsonify({'error': f'获取模型列表失败: {str(e)}'}), 500 