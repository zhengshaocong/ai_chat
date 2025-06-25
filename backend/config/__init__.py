# config包的初始化文件
# 当用户导入 config 时，这个文件会被执行

import sys
from pathlib import Path

# 自动设置项目路径（在导入任何其他模块之前）
def auto_setup_path():
    """自动设置项目路径"""
    # 如果已经在sys.path中，说明已经设置过了
    current_file = Path(__file__)
    if 'backend' in current_file.parts:
        backend_index = current_file.parts.index('backend')
        root_dir = Path(*current_file.parts[:backend_index + 1])
    else:
        root_dir = current_file.parent.parent
    
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))

# 立即执行路径设置
auto_setup_path()

# 导入路径管理
from .paths import setup_project_path, PROJECT_ROOT, CONFIG_DIR, APP_DIR, TEST_DIR, TOOLS_DIR, UTILS_DIR

import os
from pathlib import Path
from dotenv import load_dotenv

# 确定项目根目录
ROOT_DIR = Path(__file__).parent.parent  # config目录的父目录，即backend目录

# 环境配置加载
def load_env_config():
    """加载环境配置，优先加载开发环境配置"""
    env_dev_path = ROOT_DIR / '.env.development'
    env_path = ROOT_DIR / '.env'
    
    if env_dev_path.exists():
        print("加载开发环境配置文件: .env.development")
        load_dotenv(dotenv_path=env_dev_path)
        return '.env.development'
    elif env_path.exists():
        print("加载标准环境配置文件: .env")
        load_dotenv(dotenv_path=env_path)
        return '.env'
    else:
        print("警告: 未找到环境配置文件(.env.development 或 .env)")
        load_dotenv()  # 尝试加载默认位置的 .env 文件
        return 'default'

# 加载环境变量
ENV_FILE = load_env_config()

# 环境设置
ENV = os.getenv('ENV', 'development')
DEBUG = ENV == 'development'

# 应用基本配置
APP_NAME = "AI聊天助手"
APP_VERSION = "1.0.0"

# API配置
API_PREFIX = "/api"
API_VERSION = "v1"

# 导入数据库配置
from .database_config import Base, get_db, SessionLocal, engine

# 导入大模型配置
from .llm_config import *

# 定义包的公共接口
__all__ = [
    # 路径管理
    'setup_project_path', 'PROJECT_ROOT', 'CONFIG_DIR', 'APP_DIR', 'TEST_DIR', 'TOOLS_DIR', 'UTILS_DIR',
    
    # 环境配置
    'ENV', 'DEBUG', 'ENV_FILE', 'ROOT_DIR',
    'APP_NAME', 'APP_VERSION',
    'API_PREFIX', 'API_VERSION',
    
    # 数据库配置
    'Base', 'get_db', 'SessionLocal', 'engine',
    
    # LLM配置
    'DASHSCOPE_API_KEY', 'GAODE_API_KEY',
    'DEFAULT_MODEL', 'MAX_TOKENS', 'TEMPERATURE',
    'SYSTEM_PROMPT', 'MAX_HISTORY_LENGTH',
    'ENABLE_TOOL_CALLS', 'MODEL_MAPPING'
]

# 导出大模型配置中的所有变量
from .llm_config import __all__ as llm_all
__all__.extend(llm_all) 