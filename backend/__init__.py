import sys
from pathlib import Path

# 获取项目根目录
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

# 导出常用路径
__all__ = ['ROOT_DIR'] 