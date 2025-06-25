import os
import requests
import json
from typing import Dict, Any, List, Optional
from app.models.models import ChatSessionDetail
from config import get_db
from datetime import datetime
import dashscope
import time

class QwenService:
    def __init__(self, model_name: str = "qwen-turbo", test_mode: bool = False):
        # 从环境变量获取百炼平台 API Key
        self.api_key = os.getenv('BAILIAN_API_KEY')
        self.model_name = model_name
        self.test_mode = test_mode
        
        # 百炼平台API基础URL - 修正为正确的端点
        self.base_url = "https://dashscope.aliyuncs.com/api/v1"
        
    def chat_with_qwen(self, message: str, session_id: int = None, history: List[Dict] = None) -> Dict[str, Any]:
        """
        与千问进行对话（通过百炼平台）
        
        Args:
            message: 用户消息
            session_id: 会话ID（测试模式下可选）
            history: 对话历史
            
        Returns:
            Dict: 包含千问响应的字典
        """
        try:
            # 参数验证
            if not message or not message.strip():
                return {
                    "success": False,
                    "error": "消息内容不能为空"
                }
            
            if not self.api_key:
                return {
                    "success": False,
                    "error": "API密钥未设置，请检查环境变量 BAILIAN_API_KEY"
                }
            
            # 构建请求头
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 构建完整的对话内容
            full_conversation = "你是千问（Qwen），一个由阿里云开发的大语言模型。请用友好、专业的态度回答用户的问题。\n\n"
            
            # 添加历史对话
            if history:
                for msg in history:
                    if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                        if msg['role'] == 'user':
                            full_conversation += f"用户: {msg['content']}\n"
                        elif msg['role'] == 'assistant':
                            full_conversation += f"千问: {msg['content']}\n"
            
            # 添加当前用户消息
            full_conversation += f"用户: {message}\n千问:"
            
            # 构建请求体 - 使用正确的百炼平台格式
            payload = {
                "model": self.model_name,
                "input": {
                    "prompt": full_conversation
                },
                "parameters": {
                    "temperature": 0.7,
                    "max_tokens": 1500,
                    "top_p": 0.8
                }
            }
            
            # 调试信息：打印请求体
            print(f"🔍 调试信息 - 请求体:")
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            print(f"🔍 调试信息 - API URL: {self.base_url}/services/aigc/text-generation/generation")
            print(f"🔍 调试信息 - 模型: {self.model_name}")
            
            # 调用百炼平台API
            response = requests.post(
                f"{self.base_url}/services/aigc/text-generation/generation",
                headers=headers,
                data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
                timeout=30
            )
            
            print(f"🔍 调试信息 - 响应状态码: {response.status_code}")
            print(f"🔍 调试信息 - 响应内容: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('output', {}).get('text', '抱歉，我无法生成回复。')
                
                # 根据模式决定是否保存到数据库
                if not self.test_mode and session_id is not None:
                    # 正式模式：保存到数据库
                    db = next(get_db())
                    
                    # 保存用户消息到数据库
                    user_message = ChatSessionDetail(
                        chat_session_id=session_id,
                        role='user',
                        content=message,
                        created_at=datetime.utcnow()
                    )
                    db.add(user_message)
                    
                    # 保存千问回复到数据库
                    ai_message = ChatSessionDetail(
                        chat_session_id=session_id,
                        role='assistant',
                        content=ai_response,
                        created_at=datetime.utcnow()
                    )
                    db.add(ai_message)
                    
                    db.commit()
                    
                    return {
                        "success": True,
                        "message": ai_response,
                        "model_used": self.model_name,
                        "user_message_id": user_message.id,
                        "ai_message_id": ai_message.id,
                        "mode": "production"
                    }
                else:
                    # 测试模式：不保存到数据库
                    return {
                        "success": True,
                        "message": ai_response,
                        "model_used": self.model_name,
                        "mode": "test",
                        "timestamp": datetime.now().isoformat(),
                        "request_info": {
                            "model": self.model_name,
                            "temperature": payload['parameters']['temperature'],
                            "max_tokens": payload['parameters']['max_tokens']
                        }
                    }
            else:
                return {
                    "success": False,
                    "error": f"API调用失败: {response.status_code} - {response.text}"
                }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"对话失败: {str(e)}"
            }
    
    def get_available_models(self) -> List[Dict[str, str]]:
        """
        获取可用的千问模型列表（百炼平台）
        """
        models = [
            {
                "id": "qwen-turbo",
                "name": "千问 Turbo",
                "description": "快速响应，适合一般对话"
            },
            {
                "id": "qwen-plus", 
                "name": "千问 Plus",
                "description": "平衡性能和效果"
            },
            {
                "id": "qwen-max",
                "name": "千问 Max", 
                "description": "最高性能，适合复杂任务"
            }
        ]
        
        return models 