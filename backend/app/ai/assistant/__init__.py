# app/ai/assistant包的初始化文件
# 使用 ToolRegistry 进行按需注册，避免全部工具被自动注册

from .weather_assistant import WeatherAssistant, weather_assistant
from .ticket_assistant import TicketAssistant, ticket_assistant
from .data_analysis_assistant import DataAnalysisAssistant, data_analysis_assistant

__all__ = [
    'WeatherAssistant', 'weather_assistant',
    'TicketAssistant', 'ticket_assistant', 
    'DataAnalysisAssistant', 'data_analysis_assistant'
] 