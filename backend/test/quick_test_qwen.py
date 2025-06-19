#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
千问服务快速测试
直接引用app内的qwen_service，使用测试模式
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.qwen_service import QwenService

def quick_test():
    """快速测试"""
    print("🚀 千问服务快速测试")
    print("=" * 40)
    
    # 检查环境变量
    if not os.getenv('BAILIAN_API_KEY'):
        print("❌ 错误: 请设置环境变量 BAILIAN_API_KEY")
        print("请在项目根目录创建 .env 文件并添加: BAILIAN_API_KEY=你的API密钥")
        return
    
    # 创建测试服务
    service = QwenService(test_mode=True)
    
    # 测试消息
    test_message = "你好，请用一句话介绍你自己"
    print(f"📝 测试消息: {test_message}")
    print("-" * 40)
    
    # 执行测试
    result = service.chat_with_qwen(test_message)
    
    # 显示结果
    if result["success"]:
        print("✅ 测试成功!")
        print(f"🤖 千问回复: {result['message']}")
        print(f"🔧 使用模型: {result['model_used']}")
        print(f"📊 模式: {result.get('mode', 'unknown')}")
        if 'timestamp' in result:
            print(f"⏰ 测试时间: {result['timestamp']}")
    else:
        print("❌ 测试失败!")
        print(f"错误信息: {result['error']}")
    
    print("=" * 40)

def interactive_test():
    """交互式测试"""
    print("💬 千问服务交互式测试")
    print("输入 'quit' 或 'exit' 退出")
    print("=" * 40)
    
    # 检查环境变量
    if not os.getenv('BAILIAN_API_KEY'):
        print("❌ 错误: 请设置环境变量 BAILIAN_API_KEY")
        return
    
    # 创建测试服务
    service = QwenService(test_mode=True)
    history = []
    
    while True:
        try:
            # 获取用户输入
            user_input = input("\n👤 你: ").strip()
            
            # 检查退出命令
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("👋 再见!")
                break
            
            if not user_input:
                print("⚠️  请输入消息")
                continue
            
            print("🤔 千问正在思考...")
            
            # 调用模型
            result = service.chat_with_qwen(user_input, history=history)
            
            if result["success"]:
                print(f"🤖 千问: {result['message']}")
                # 更新历史对话
                history.append({"role": "user", "content": user_input})
                history.append({"role": "assistant", "content": result['message']})
            else:
                print(f"❌ 错误: {result['error']}")
                
        except KeyboardInterrupt:
            print("\n👋 再见!")
            break
        except Exception as e:
            print(f"❌ 发生错误: {str(e)}")

def test_with_custom_history():
    """测试自定义历史对话"""
    print("📚 测试自定义历史对话")
    print("=" * 40)
    
    # 检查环境变量
    if not os.getenv('BAILIAN_API_KEY'):
        print("❌ 错误: 请设置环境变量 BAILIAN_API_KEY")
        return
    
    # 创建测试服务
    service = QwenService(test_mode=True)
    
    # 自定义历史对话
    history = [
        {"role": "user", "content": "我想学习编程"},
        {"role": "assistant", "content": "学习编程是一个很好的选择！建议从Python开始，它语法简单，适合初学者。"},
        {"role": "user", "content": "Python有什么特点？"},
        {"role": "assistant", "content": "Python的特点包括：语法简洁、可读性强、跨平台、丰富的库支持、适合快速开发等。"}
    ]
    
    # 测试新消息
    test_message = "请推荐一些Python学习资源"
    print(f"📝 测试消息: {test_message}")
    print(f"📚 历史对话数量: {len(history)}")
    print("-" * 40)
    
    result = service.chat_with_qwen(test_message, history=history)
    
    if result["success"]:
        print("✅ 测试成功!")
        print(f"🤖 千问回复: {result['message']}")
        print(f"🔧 使用模型: {result['model_used']}")
        print(f"📊 模式: {result.get('mode', 'unknown')}")
    else:
        print("❌ 测试失败!")
        print(f"错误信息: {result['error']}")
    
    print("=" * 40)

def main():
    """主函数"""
    print("选择测试模式:")
    print("1. 快速测试")
    print("2. 交互式测试")
    print("3. 自定义历史对话测试")
    print("4. 完整测试")
    
    choice = input("\n请选择 (1/2/3/4): ").strip()
    
    if choice == "1":
        quick_test()
    elif choice == "2":
        interactive_test()
    elif choice == "3":
        test_with_custom_history()
    elif choice == "4":
        # 运行完整测试
        from test.test_qwen_service import main as run_full_test
        run_full_test()
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main() 