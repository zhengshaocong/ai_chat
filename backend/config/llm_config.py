import os

def safe_int(value, default):
    """安全地将值转换为整数，如果转换失败则返回默认值"""
    if value is None or value == '':
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default):
    """安全地将值转换为浮点数，如果转换失败则返回默认值"""
    if value is None or value == '':
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

# 通义千问API配置
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

# 模型参数配置
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen-turbo")  # 默认使用通义千问turbo模型
MAX_TOKENS = safe_int(os.getenv("MAX_TOKENS"), 1500)  # 生成的最大token数
TEMPERATURE = safe_float(os.getenv("TEMPERATURE"), 0.7)  # 温度参数，控制创造性/随机性

# 高德地图API，用于天气查询等工具函数
GAODE_API_KEY = os.getenv("GAODE_API_KEY")

# 定义系统角色提示词
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "你是一个有用的AI助手，可以回答用户的各类问题。")

# 历史记录配置
MAX_HISTORY_LENGTH = safe_int(os.getenv("MAX_HISTORY_LENGTH"), 10)  # 保留的最大对话轮数

# 工具调用配置
ENABLE_TOOL_CALLS = os.getenv("ENABLE_TOOL_CALLS", "true").lower() == "true"

# 模型ID映射，便于通过名称选择模型
MODEL_MAPPING = {
    "qwen-turbo": "qwen-turbo",
    "qwen-plus": "qwen-plus",
    "qwen-max": "qwen-max",
    "qwen-max-longcontext": "qwen-max-longcontext",
}

# 导出所有变量
__all__ = [
    'DASHSCOPE_API_KEY',
    'DEFAULT_MODEL',
    'MAX_TOKENS',
    'TEMPERATURE',
    'GAODE_API_KEY',
    'SYSTEM_PROMPT',
    'MAX_HISTORY_LENGTH',
    'ENABLE_TOOL_CALLS',
    'MODEL_MAPPING',
]