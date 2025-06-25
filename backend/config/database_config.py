import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# 由于这个文件会被index.py导入，因此不再需要在这里加载环境变量
# 在import这个模块前，index.py已经加载了环境变量

def safe_int(value, default):
    """安全地将值转换为整数，如果转换失败则返回默认值"""
    if value is None or value == '':
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

# 从环境变量获取数据库配置，提供默认值
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = safe_int(os.getenv('DB_PORT'), 3306)
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'xxxx')
DB_NAME = os.getenv('DB_NAME', 'ai_chat')

# 构建数据库URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{str(DB_PORT)}/{DB_NAME}"
print(DATABASE_URL)
# 添加连接参数
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    connect_args={
        'connect_timeout': 10,
        'read_timeout': 30,
        'write_timeout': 30
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 