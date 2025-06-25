from qwen_agent.gui import WebUI
from app.ai.assistant import weather_assistant, ticket_assistant, data_analysis_assistant, WeatherAssistant, TicketAssistant, DataAnalysisAssistant
import os

assistant_list = {
    "weather": {
        "assistant": weather_assistant,
        "title": "欢迎使用天气智能助手！(输入 'exit' 退出)",
    },
    "ticket": {
        "assistant": ticket_assistant,
        "title": "欢迎使用门票智能助手！(输入 'exit' 退出)",
    },
    "data_analysis": {
        "assistant": data_analysis_assistant,
        "title": "欢迎使用数据分析助手！(输入 'exit' 退出)",
    }
}

# 也可以直接使用类
assistant_classes = {
    "weather": WeatherAssistant,
    "ticket": TicketAssistant,
    "data_analysis": DataAnalysisAssistant,
}

active = 'data_analysis'  # 默认使用数据分析助手

def app_tui():
    try:
        # 使用工厂函数方式（原有方式）
        bot = assistant_list[active]['assistant']()
        messages = []
        print(assistant_list[active]['title'])
        while True:
            try:
                query = input('\n请输入您的问题: ')
                if query.lower() == 'exit':
                    break
                if not query:
                    continue
                messages.append({'role': 'user', 'content': query})
                response = []
                last_reply = None
                for group in bot.run(messages):
                    for resp in group:
                        if hasattr(resp, 'get') and resp.get('role') == 'assistant' and resp.get('content'):
                            last_reply = resp.get('content')
                if not last_reply:
                    messages.append({'role': 'user', 'content': ''})
                    for group in bot.run(messages):
                        for resp in group:
                            if hasattr(resp, 'get') and resp.get('role') == 'assistant' and resp.get('content'):
                                last_reply = resp.get('content')
                if last_reply:
                    print(last_reply)
                messages.extend(response)
            except Exception as e:
                print(f"发生错误: {str(e)}")
    except Exception as e:
        print(f"启动终端模式失败: {str(e)}")

def app_gui():
    try:
        # 使用工厂函数方式（原有方式）
        bot = assistant_list[active]['assistant']()
        chatbot_config = {
            'prompt.suggestions': [
                '查询2023年各月份的门票销量',
                '分析不同省份的入园人数分布',
                '生成销售渠道订单金额的柱状图',
                '查看门票类型销量占比的饼图'
            ]
        }
        print("Web 界面准备就绪，正在启动服务...")
        WebUI(
            bot,
            chatbot_config=chatbot_config
        ).run()
    except Exception as e:
        print(f"启动 Web 界面失败: {str(e)}")
        print("请检查网络连接和 API Key 配置")

def app_tui_with_class():
    """使用类方式的终端交互"""
    try:
        # 使用类方式
        assistant_class = assistant_classes[active]
        bot = assistant_class()
        messages = []
        print(assistant_list[active]['title'])
        while True:
            try:
                query = input('\n请输入您的问题: ')
                if query.lower() == 'exit':
                    break
                if not query:
                    continue
                # 使用类的chat方法
                response = bot.chat(query)
                for group in response:
                    for resp in group:
                        if hasattr(resp, 'get') and resp.get('role') == 'assistant' and resp.get('content'):
                            print(resp.get('content'))
            except Exception as e:
                print(f"发生错误: {str(e)}")
    except Exception as e:
        print(f"启动终端模式失败: {str(e)}")

def select_assistant():
    """选择助手"""
    global active
    print("\n请选择助手：")
    print("1. 天气助手")
    print("2. 门票助手")
    print("3. 数据分析助手")
    while True:
        choice = input("请输入选择 (1, 2 或 3): ").strip()
        if choice == '1':
            active = 'weather'
            break
        elif choice == '2':
            active = 'ticket'
            break
        elif choice == '3':
            active = 'data_analysis'
            break
        else:
            print("无效选择，请输入 1, 2 或 3")

def main():
    select_assistant()
    print("请选择运行模式：")
    print("1. 终端交互模式（工厂函数）")
    print("2. Web图形界面模式")
    print("3. 终端交互模式（类方式）")
    while True:
        choice = input("请输入选择 (1, 2 或 3): ").strip()
        if choice == '1':
            app_tui()
            break
        elif choice == '2':
            app_gui()
            break
        elif choice == '3':
            app_tui_with_class()
            break
        else:
            print("无效选择，请输入 1, 2 或 3")

if __name__ == "__main__":
    main() 