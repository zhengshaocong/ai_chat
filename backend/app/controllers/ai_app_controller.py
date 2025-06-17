from flask import Blueprint, jsonify, request
from app.services.ai_app_service import AIAppService
from config.database import get_db

ai_app_bp = Blueprint('ai_app', __name__)
ai_app_service = AIAppService()

@ai_app_bp.route('/', methods=['GET'])
def get_all_ai_apps():
    db = next(get_db())
    apps = ai_app_service.get_all_ai_apps(db)
    return jsonify([{
        'id': app.id,
        'name': app.name,
        'description': app.description,
        'icon': app.icon
    } for app in apps])

@ai_app_bp.route('/<int:app_id>', methods=['GET'])
def get_ai_app(app_id):
    db = next(get_db())
    app = ai_app_service.get_ai_app_by_id(db, app_id)
    if not app:
        return jsonify({'error': 'AI应用不存在'}), 404
    return jsonify({
        'id': app.id,
        'name': app.name,
        'description': app.description,
        'icon': app.icon
    }) 