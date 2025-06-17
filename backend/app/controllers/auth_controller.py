from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from functools import wraps
import jwt
from flask import current_app

auth_bp = Blueprint('auth', __name__)

def success_response(data=None, message=None, status_code=200):
    """成功响应"""
    response = {'code': 0}
    if message:
        response['message'] = message
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

def error_response(message, status_code=400, code=1):
    """错误响应"""
    return jsonify({
        'code': code,
        'message': message
    }), status_code

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return error_response('缺少认证令牌', 401)
        
        try:
            token = token.split(' ')[1]  # 移除 'Bearer ' 前缀
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = AuthService.get_user_by_id(data['user_id'])
            
            if not current_user:
                return error_response('无效的认证令牌', 401)
                
        except Exception as e:
            return error_response('无效的认证令牌', 401)
            
        return f(current_user, *args, **kwargs)
    
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        print("收到注册请求")
        print("请求方法:", request.method)
        print("请求路径:", request.path)
        print("原始数据:", request.get_data())
        
        data = request.get_json()
        print("解析后的JSON数据:", data)
        
        if not data:
            return error_response('请求体不能为空')
            
        if not isinstance(data, dict):
            return error_response('请求体必须是JSON对象')
        
        if not all(k in data for k in ('username', 'password')):
            missing = [k for k in ('username', 'password') if k not in data]
            return error_response(f'缺少必要的注册信息: {", ".join(missing)}')
        
        if not data['username'] or not data['password']:
            return error_response('用户名和密码不能为空')
        
        success, message = AuthService.register(
            data['username'],
            data['password']
        )
        
        if success:
            return success_response(message=message, status_code=201)
        else:
            return error_response(message)
    except Exception as e:
        print("注册异常:", str(e))
        return error_response(f'注册失败: {str(e)}')

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        print("收到登录请求")
        print("请求方法:", request.method)
        print("请求路径:", request.path)
        print("原始数据:", request.get_data())
        
        data = request.get_json()
        print("解析后的JSON数据:", data)
        
        if not data:
            return error_response('请求体不能为空')
            
        if not isinstance(data, dict):
            return error_response('请求体必须是JSON对象')
        
        if not all(k in data for k in ('username', 'password')):
            missing = [k for k in ('username', 'password') if k not in data]
            return error_response(f'缺少必要的登录信息: {", ".join(missing)}')
        
        if not data['username'] or not data['password']:
            return error_response('用户名和密码不能为空')
        
        success, result = AuthService.login(
            data['username'],
            data['password']
        )
        
        if success:
            return success_response(data=result)
        else:
            return error_response(result, 401)
    except Exception as e:
        print("登录异常:", str(e))
        return error_response(f'登录失败: {str(e)}')

@auth_bp.route('/user', methods=['GET'])
@token_required
def get_user_info(current_user):
    return success_response(data={
        'id': current_user.id,
        'username': current_user.username
    })

@auth_bp.route('/user', methods=['PUT'])
@token_required
def update_user_info(current_user):
    try:
        data = request.get_json()
        if not data:
            return error_response('请求体不能为空')
            
        # 这里可以添加更新用户信息的逻辑
        return success_response(message='更新成功')
    except Exception as e:
        return error_response(f'更新失败: {str(e)}')

@auth_bp.route('/password', methods=['PUT'])
@token_required
def update_password(current_user):
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ('old_password', 'new_password')):
            return error_response('缺少必要的密码信息')
            
        # 这里可以添加更新密码的逻辑
        return success_response(message='密码更新成功')
    except Exception as e:
        return error_response(f'密码更新失败: {str(e)}')

@auth_bp.route('/avatar', methods=['POST'])
@token_required
def upload_avatar(current_user):
    try:
        if 'file' not in request.files:
            return error_response('没有上传文件')
            
        file = request.files['file']
        if file.filename == '':
            return error_response('没有选择文件')
            
        # 这里可以添加处理头像上传的逻辑
        return success_response(data={'url': 'avatar_url_here'})
    except Exception as e:
        return error_response(f'头像上传失败: {str(e)}')

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    # 由于使用 JWT，服务器端不需要处理登出
    # 客户端只需要删除 token 即可
    return success_response(message='登出成功') 