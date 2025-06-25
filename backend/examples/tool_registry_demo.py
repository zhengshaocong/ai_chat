"""
工具注册管理器使用示例
演示如何按需注册工具，避免全部工具被自动注册
"""

from app.ai.tool.registry import ToolRegistry

def demo_weather_assistant():
    """演示天气助手的工具注册"""
    print("=== 天气助手工具注册演示 ===")
    
    # 只注册天气工具
    weather_tool = ToolRegistry.register_weather_tool()
    print(f"已注册天气工具: {weather_tool}")
    
    # 检查工具是否可用
    from app.ai.assistant import WeatherAssistant
    assistant = WeatherAssistant()
    print(f"天气助手可用工具: {assistant.get_available_tools()}")
    print()

def demo_ticket_assistant():
    """演示门票助手的工具注册"""
    print("=== 门票助手工具注册演示 ===")
    
    # 只注册SQL工具
    sql_tool = ToolRegistry.register_sql_tool()
    print(f"已注册SQL工具: {sql_tool}")
    
    # 检查工具是否可用
    from app.ai.assistant import TicketAssistant
    assistant = TicketAssistant()
    print(f"门票助手可用工具: {assistant.get_available_tools()}")
    print()

def demo_data_analysis_assistant():
    """演示数据分析助手的工具注册"""
    print("=== 数据分析助手工具注册演示 ===")
    
    # 只注册SQL转图表工具
    sql_chart_tool = ToolRegistry.register_sql_chart_tool()
    print(f"已注册SQL转图表工具: {sql_chart_tool}")
    
    # 检查工具是否可用
    from app.ai.assistant import DataAnalysisAssistant
    assistant = DataAnalysisAssistant()
    print(f"数据分析助手可用工具: {assistant.get_available_tools()}")
    print()

def demo_batch_registration():
    """演示批量工具注册"""
    print("=== 批量工具注册演示 ===")
    
    # 批量注册多个工具
    tools = ToolRegistry.register_tools('weather', 'sql', 'chart')
    print(f"批量注册的工具: {list(tools.keys())}")
    
    # 验证工具是否正确注册
    for tool_name, tool_class in tools.items():
        print(f"  {tool_name}: {tool_class}")
    print()

def demo_selective_registration():
    """演示选择性工具注册"""
    print("=== 选择性工具注册演示 ===")
    
    # 根据需求选择性注册工具
    needed_tools = ['weather', 'sql_chart']  # 只注册需要的工具
    tools = ToolRegistry.register_tools(*needed_tools)
    print(f"选择性注册的工具: {list(tools.keys())}")
    print()

if __name__ == "__main__":
    print("工具注册管理器演示")
    print("=" * 50)
    
    # 演示各种注册方式
    demo_weather_assistant()
    demo_ticket_assistant()
    demo_data_analysis_assistant()
    demo_batch_registration()
    demo_selective_registration()
    
    print("演示完成！")
    print("\n优势总结：")
    print("1. 按需注册：只注册需要的工具，避免全部工具被自动注册")
    print("2. 灵活控制：可以根据不同助手的需求选择性注册工具")
    print("3. 性能优化：减少不必要的工具加载和注册")
    print("4. 清晰管理：通过 ToolRegistry 统一管理工具注册") 