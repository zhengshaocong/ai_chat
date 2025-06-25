import dashscope
from qwen_agent.agents import Assistant
from config import DASHSCOPE_API_KEY
from ..tool import ToolRegistry  # 使用工具注册管理器

system_prompt = """我是天气助手，专门用于查询天气信息。

我可以帮助你：
1. 查询指定城市的当前天气
2. 提供温度、湿度、风力等详细信息
3. 给出天气建议

请告诉我你想查询哪个城市的天气信息。"""

class WeatherAssistant:
    def __init__(self, model='qwen-turbo', timeout=30, retry_count=3):
        self.model = model
        self.timeout = timeout
        self.retry_count = retry_count
        self.bot = None
        self._init_assistant()
    
    def _init_assistant(self):
        """初始化助手"""
        if not DASHSCOPE_API_KEY:
            raise ValueError("请在环境配置中设置 DASHSCOPE_API_KEY")
        
        dashscope.api_key = DASHSCOPE_API_KEY
        dashscope.timeout = self.timeout

        llm_cfg = {
            'model': self.model,
            'timeout': self.timeout,
            'retry_count': self.retry_count,
        }
        
        # 注册工具：get_current_weather
        ToolRegistry.register_weather_tool()
        
        # 定义可用的工具列表
        available_tools = ['get_current_weather']
        
        self.bot = Assistant(
            llm=llm_cfg,
            name='天气助手',
            description='专业的天气查询助手',
            system_message=system_prompt,
            function_list=available_tools,  # 使用明确的工具列表
        )
    
    def run(self, messages):
        """运行助手"""
        return self.bot.run(messages)
    
    def chat(self, message):
        """单次对话"""
        messages = [{'role': 'user', 'content': message}]
        return self.run(messages)
    
    def get_available_tools(self):
        """获取可用工具列表"""
        return ['get_current_weather']
    
    def get_weather(self, city):
        """便捷的天气查询方法"""
        message = f"请查询{city}的天气信息"
        return self.chat(message)

# 工厂函数，保持向后兼容
def weather_assistant():
    return WeatherAssistant().bot
