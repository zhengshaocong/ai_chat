import dashscope
from qwen_agent.agents import Assistant
from config import DASHSCOPE_API_KEY
from ..tool import ToolRegistry  # 使用工具注册管理器

system_prompt = system_prompt = """我是门票助手，以下是关于门票订单表相关的字段，我可能会编写对应的SQL，对数据进行查询
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
"""

class TicketAssistant:
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
        
        # 按需注册工具
        # 只注册门票助手需要的工具
        ToolRegistry.register_sql_tool()
        
        # 定义可用的工具列表
        # exc_sql: 通过 ToolRegistry 按需注册
        available_tools = ['exc_sql']
        
        self.bot = Assistant(
            llm=llm_cfg,
            name='门票助手',
            description='专业的门票查询助手',
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
        return ['exc_sql']
    
    def query_tickets(self, query):
        """便捷的门票查询方法"""
        message = f"请查询门票信息：{query}"
        return self.chat(message)

# 工厂函数，保持向后兼容
def ticket_assistant():
    return TicketAssistant().bot 