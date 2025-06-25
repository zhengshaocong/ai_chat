import sys
from pathlib import Path

def setup_project_path():
    """设置项目路径，确保可以导入项目模块"""
    # 获取当前文件所在目录
    current_file = Path(__file__)
    
    # 根据文件位置确定项目根目录
    if 'backend' in current_file.parts:
        # 如果在backend目录下
        backend_index = current_file.parts.index('backend')
        root_dir = Path(*current_file.parts[:backend_index + 1])
    else:
        # 默认情况
        root_dir = current_file.parent.parent
    
    # 添加到Python路径
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))
    
    return root_dir

# 自动设置路径
PROJECT_ROOT = setup_project_path()

# 常用路径常量
CONFIG_DIR = PROJECT_ROOT / 'config'
APP_DIR = PROJECT_ROOT / 'app'
TEST_DIR = PROJECT_ROOT / 'test'
TOOLS_DIR = APP_DIR / 'tool'

# 常用路径
UTILS_DIR = PROJECT_ROOT / 'utils' 