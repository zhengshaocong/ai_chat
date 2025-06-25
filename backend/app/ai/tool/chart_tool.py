from qwen_agent.tools.base import BaseTool, register_tool
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import json
import numpy as np
import os
import uuid

@register_tool('generate_chart')
class ChartTool(BaseTool):
    """
    图表生成工具，将数据转换为各种图表
    """
    description = '将数据转换为图表，支持柱状图、折线图、饼图等'
    parameters = [{
        'name': 'data',
        'type': 'string',
        'description': '数据，可以是JSON格式的数组或CSV格式的字符串',
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
        'name': 'data_format',
        'type': 'string',
        'description': '数据格式：json或csv，默认为json',
        'required': False
    }]

    def call(self, params: str, **kwargs) -> str:
        try:
            args = json.loads(params)
            data = args['data']
            chart_type = args['chart_type']
            x_column = args['x_column']
            y_column = args.get('y_column')
            title = args.get('title', '数据图表')
            data_format = args.get('data_format', 'json')
            
            # 解析数据
            df = self._parse_data(data, data_format)
            
            if df.empty:
                return "数据为空，无法生成图表"
            
            # 检查列是否存在
            if x_column not in df.columns:
                return f"错误：列 '{x_column}' 不存在于数据中。可用列：{list(df.columns)}"
            
            if y_column and y_column not in df.columns:
                return f"错误：列 '{y_column}' 不存在于数据中。可用列：{list(df.columns)}"
            
            # 生成图表并保存为文件
            plt = self._generate_chart(df, chart_type, x_column, y_column, title, return_plt=True)
            # 自动创建目录（以当前文件为基准，绝对路径）
            base_dir = os.path.dirname(os.path.abspath(__file__))
            static_dir = os.path.join(base_dir, '../../../static/tmp/tool/chart_tool')
            static_dir = os.path.abspath(static_dir)
            os.makedirs(static_dir, exist_ok=True)
            filename = f"{uuid.uuid4().hex}.png"
            file_path = os.path.join(static_dir, filename)
            plt.savefig(file_path, format='png', dpi=300, bbox_inches='tight')
            plt.close()
            # 生成图片URL（指向Flask静态服务）
            url_path = f"http://127.0.0.1:9000/static/tmp/tool/chart_tool/{filename}"
            print('chart_image file:', file_path)
            
            # 返回图表信息
            # result = {
            #     'success': True,
            #     'chart_type': chart_type,
            #     'data_preview': df.head(5).to_dict('records'),
            #     'chart_image': url_path,
            #     'message': f'成功生成{chart_type}图表，数据行数：{len(df)}'
            # }
            # return json.dumps(result, ensure_ascii=False, indent=2)
            return f"成功生成图表：<br><img src=\"{url_path}\" style=\"max-width: 100%; height: auto;\">"
            
        except Exception as e:
            return f"生成图表时出错: {str(e)}"
    
    def _parse_data(self, data, data_format):
        """解析数据"""
        try:
            if data_format.lower() == 'json':
                # 解析JSON数据
                if isinstance(data, str):
                    data_list = json.loads(data)
                else:
                    data_list = data
                return pd.DataFrame(data_list)
            
            elif data_format.lower() == 'csv':
                # 解析CSV数据
                from io import StringIO
                return pd.read_csv(StringIO(data))
            
            else:
                raise ValueError(f"不支持的数据格式：{data_format}")
                
        except Exception as e:
            raise Exception(f"数据解析失败: {str(e)}")
    
    def _generate_chart(self, df, chart_type, x_column, y_column, title, return_plt=False):
        """生成具体图表"""
        plt.figure(figsize=(12, 8))
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']  # 支持中文
        plt.rcParams['axes.unicode_minus'] = False
        
        try:
            if chart_type == 'bar':
                if y_column:
                    plt.bar(df[x_column], df[y_column])
                else:
                    plt.bar(df[x_column], df.iloc[:, 1])  # 使用第二列作为Y值
                plt.xticks(rotation=45)
                
            elif chart_type == 'line':
                if y_column:
                    plt.plot(df[x_column], df[y_column], marker='o')
                else:
                    plt.plot(df[x_column], df.iloc[:, 1], marker='o')
                plt.xticks(rotation=45)
                
            elif chart_type == 'pie':
                if y_column:
                    plt.pie(df[y_column], labels=df[x_column], autopct='%1.1f%%')
                else:
                    plt.pie(df.iloc[:, 1], labels=df[x_column], autopct='%1.1f%%')
                    
            elif chart_type == 'scatter':
                if y_column:
                    plt.scatter(df[x_column], df[y_column])
                else:
                    plt.scatter(df[x_column], df.iloc[:, 1])
                plt.xticks(rotation=45)
                
            elif chart_type == 'heatmap':
                # 热力图需要数值型数据
                numeric_df = df.select_dtypes(include=[np.number])
                if len(numeric_df.columns) >= 2:
                    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
                else:
                    raise Exception("热力图需要至少两个数值型列")
            else:
                raise Exception(f"不支持的图表类型：{chart_type}")
            
            plt.title(title)
            plt.tight_layout()
            
            if return_plt:
                return plt
            
            # 将图表转换为base64字符串
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            chart_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return chart_base64
            
        except Exception as e:
            plt.close()
            raise Exception(f"生成{chart_type}图表失败: {str(e)}") 