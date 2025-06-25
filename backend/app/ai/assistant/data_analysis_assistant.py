import dashscope
from qwen_agent.agents import Assistant
from config import DASHSCOPE_API_KEY
from ..tool import ToolRegistry  # 使用工具注册管理器

system_prompt = """我是门票助手，专门用于查询门票相关数据。也可以将数据转化为图表

我可以帮助你：
1. 执行SQL查询获取数据
2. 将数据转换为各种图表（柱状图、折线图、饼图、散点图、热力图）
3. 一键完成SQL查询和图表生成

SQL信息
-- 门票订单表
CREATE TABLE tkt_orders (
    order_time DATETIME,             -- 订单日期
    account_id INT,                  -- 预定用户ID
    gov_id VARCHAR(18),              -- 商品使用人ID（身份证号）
    gender VARCHAR(10),              -- 使用人性别
    age INT,                         -- 年龄
    province VARCHAR(30),           -- 使用人省份
    SKU VARCHAR(100),                -- 商品SKU名
    product_serial_no VARCHAR(30),  -- 商品ID
    eco_main_order_id VARCHAR(20),  -- 订单ID
    sales_channel VARCHAR(20),      -- 销售渠道
    status VARCHAR(30),             -- 商品状态
    order_value DECIMAL(10,2),       -- 订单金额
    quantity INT                     -- 商品数量
);
一日门票，对应多种SKU：
Universal Studios Beijing One-Day Dated Ticket-Standard
Universal Studios Beijing One-Day Dated Ticket-Child
Universal Studios Beijing One-Day Dated Ticket-Senior
二日门票，对应多种SKU：
USB 1.5-Day Dated Ticket Standard
USB 1.5-Day Dated Ticket Discounted
一日门票、二日门票查询
SUM(CASE WHEN SKU LIKE 'Universal Studios Beijing One-Day%' THEN quantity ELSE 0 END) AS one_day_ticket_sales,
SUM(CASE WHEN SKU LIKE 'USB%' THEN quantity ELSE 0 END) AS two_day_ticket_sales
我将回答用户关于门票相关的问题

可用的图表类型：
- bar: 柱状图（适合分类数据对比）
- line: 折线图（适合时间序列数据）
- pie: 饼图（适合占比分析）
- scatter: 散点图（适合相关性分析）
- heatmap: 热力图（适合相关性矩阵）

使用建议：
- 对于销售数据，建议使用柱状图或折线图
- 对于占比分析，建议使用饼图
- 对于趋势分析，建议使用折线图
- 对于相关性分析，建议使用散点图或热力图

我会根据你的需求选择最合适的图表类型来帮助你进行数据分析。"""

class DataAnalysisAssistant:
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
        
        # 注册工具：sql_to_chart
        ToolRegistry.register_sql_chart_tool()
        
        # 定义可用的工具列表
        # sql_to_chart: 通过 ToolRegistry 按需注册
        available_tools = ['sql_to_chart']
        
        self.bot = Assistant(
            llm=llm_cfg,
            name='数据分析助手',
            description='专业的数据查询和可视化分析助手',
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
        return ['sql_to_chart']
    
    def analyze_data(self, sql_query, chart_type='auto', title=None):
        """便捷的数据分析方法"""
        message = f"请帮我分析以下数据：\nSQL查询：{sql_query}"
        if chart_type != 'auto':
            message += f"\n图表类型：{chart_type}"
        if title:
            message += f"\n图表标题：{title}"
        
        return self.chat(message)

# 工厂函数，保持向后兼容
def data_analysis_assistant():
    return DataAnalysisAssistant().bot 