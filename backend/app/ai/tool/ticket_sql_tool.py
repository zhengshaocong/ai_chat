from qwen_agent.tools.base import BaseTool, register_tool
import pandas as pd
from sqlalchemy import create_engine

@register_tool('exc_sql')
class ExcSQLTool(BaseTool):
    """
    SQL查询工具，执行传入的SQL语句并返回结果。
    """
    description = '对于生成的SQL，进行SQL查询'
    parameters = [{
        'name': 'sql_input',
        'type': 'string',
        'description': '生成的SQL语句',
        'required': True
    }]

    def call(self, params: str, **kwargs) -> str:
        import json
        args = json.loads(params)
        sql_input = args['sql_input']
        database = args.get('database', 'ubr')
        # 创建数据库连接
        engine = create_engine(
            f'mysql+mysqlconnector://student123:student321@rm-uf6z891lon6dxuqblqo.mysql.rds.aliyuncs.com:3306/{database}?charset=utf8mb4',
            connect_args={'connect_timeout': 10}, pool_size=10, max_overflow=20
        )
        try:
            df = pd.read_sql(sql_input, engine)
            # 返回前10行，防止数据过多
            return df.head(10).to_markdown(index=False)
        except Exception as e:
            return f"SQL执行出错: {str(e)}" 