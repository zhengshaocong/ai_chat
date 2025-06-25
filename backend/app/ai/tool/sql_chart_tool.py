from qwen_agent.tools.base import BaseTool, register_tool
import pandas as pd
import json
from .ticket_sql_tool import ExcSQLTool
from .chart_tool import ChartTool

@register_tool('sql_to_chart')
class SQLChartTool(BaseTool):
    """
    SQL查询并生成图表工具，结合SQL查询和图表生成功能
    """
    description = '执行SQL查询并将结果转换为图表，支持柱状图、折线图、饼图等'
    parameters = [{
        'name': 'sql_input',
        'type': 'string',
        'description': 'SQL查询语句',
        'required': True
    }, {
        'name': 'chart_type',
        'type': 'string',
        'description': '图表类型：bar(柱状图)、line(折线图)、pie(饼图)、scatter(散点图)、heatmap(热力图)',
        'required': True
    }, {
        'name': 'x_column',
        'type': 'string',
        'description': 'X轴列名',
        'required': True
    }, {
        'name': 'y_column',
        'type': 'string',
        'description': 'Y轴列名（饼图不需要）',
        'required': False
    }, {
        'name': 'title',
        'type': 'string',
        'description': '图表标题',
        'required': False
    }, {
        'name': 'database',
        'type': 'string',
        'description': '数据库名，默认为ubr',
        'required': False
    }]

    def __init__(self, *args, **kwargs):
        super().__init__()
        # 初始化子工具
        self.sql_tool = ExcSQLTool()
        self.chart_tool = ChartTool()

    def call(self, params: str, **kwargs) -> str:
        try:
            args = json.loads(params)
            sql_input = args['sql_input']
            chart_type = args['chart_type']
            x_column = args['x_column']
            y_column = args.get('y_column')
            title = args.get('title', 'SQL查询结果图表')
            database = args.get('database', 'ubr')
            
            # 第一步：执行SQL查询
            sql_params = json.dumps({
                'sql_input': sql_input,
                'database': database
            })
            sql_result = self.sql_tool.call(sql_params)
            
            # 检查SQL查询是否成功
            if "SQL执行出错" in sql_result or "错误" in sql_result:
                return f"SQL查询失败: {sql_result}"
            
            # 第二步：解析SQL查询结果
            try:
                # SQL工具返回的是markdown格式，需要解析为数据
                df = self._parse_sql_result(sql_result)
                if df.empty:
                    return "SQL查询结果为空，无法生成图表"
            except Exception as e:
                return f"解析SQL结果失败: {str(e)}"
            
            # 第三步：检查列是否存在
            if x_column not in df.columns:
                return f"错误：列 '{x_column}' 不存在于查询结果中。可用列：{list(df.columns)}"
            
            if y_column and y_column not in df.columns:
                return f"错误：列 '{y_column}' 不存在于查询结果中。可用列：{list(df.columns)}"
            
            # 第四步：生成图表
            chart_params = json.dumps({
                'data': df.to_dict('records'),
                'chart_type': chart_type,
                'x_column': x_column,
                'y_column': y_column,
                'title': title,
                'data_format': 'json'
            })
            
            chart_result = self.chart_tool.call(chart_params)
            
            # 返回组合结果
            result = {
                'sql_query': sql_input,
                'sql_result': sql_result,
                'chart_result': chart_result,
                'message': f'成功执行SQL查询并生成{chart_type}图表'
            }
            
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        except Exception as e:
            return f"SQL转图表工具执行出错: {str(e)}"
    
    def _parse_sql_result(self, sql_result):
        """解析SQL查询结果（markdown格式）为DataFrame"""
        try:
            # 如果SQL结果包含markdown表格，解析它
            if '|' in sql_result:
                lines = sql_result.strip().split('\n')
                # 找到表格开始和结束
                table_lines = []
                in_table = False
                
                for line in lines:
                    if '|' in line and not line.startswith('---'):
                        table_lines.append(line)
                    elif line.startswith('---'):
                        in_table = True
                
                if table_lines:
                    # 解析markdown表格
                    headers = [h.strip() for h in table_lines[0].split('|')[1:-1]]
                    data = []
                    for line in table_lines[1:]:
                        row = [cell.strip() for cell in line.split('|')[1:-1]]
                        if len(row) == len(headers):
                            data.append(row)
                    
                    return pd.DataFrame(data, columns=headers)
            
            # 如果无法解析markdown，尝试其他格式
            # 这里可以添加更多解析逻辑
            raise Exception("无法解析SQL查询结果格式")
            
        except Exception as e:
            raise Exception(f"解析SQL结果失败: {str(e)}") 