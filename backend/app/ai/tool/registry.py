"""
工具注册管理器
实现按需注册，避免全部工具被自动注册
"""

class ToolRegistry:
    """工具注册管理器"""
    
    @staticmethod
    def register_weather_tool():
        """注册天气工具"""
        from .weather_tool import WeatherTool
        return WeatherTool
    
    @staticmethod
    def register_sql_tool():
        """注册SQL查询工具"""
        from .ticket_sql_tool import ExcSQLTool
        return ExcSQLTool
    
    @staticmethod
    def register_chart_tool():
        """注册图表工具"""
        from .chart_tool import ChartTool
        return ChartTool
    
    @staticmethod
    def register_sql_chart_tool():
        """注册SQL转图表工具"""
        from .sql_chart_tool import SQLChartTool
        return SQLChartTool
    
    @staticmethod
    def register_tools(*tool_names):
        """批量注册指定工具"""
        tools = {}
        for tool_name in tool_names:
            if tool_name == 'weather':
                tools['get_current_weather'] = ToolRegistry.register_weather_tool()
            elif tool_name == 'sql':
                tools['exc_sql'] = ToolRegistry.register_sql_tool()
            elif tool_name == 'chart':
                tools['generate_chart'] = ToolRegistry.register_chart_tool()
            elif tool_name == 'sql_chart':
                tools['sql_to_chart'] = ToolRegistry.register_sql_chart_tool()
        return tools 