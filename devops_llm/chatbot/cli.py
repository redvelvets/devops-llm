"""
聊天机器人命令行界面
"""
import sys
import json
from typing import Dict, Any

from loguru import logger
from chatbot import Chatbot

def display_bot_response(response_data: Dict[str, Any]) -> None:
    """
    显示机器人的响应
    """
    # 显示工具调用信息（如果有）
    if response_data["tool_calls"]:
        print("\n🔧 使用了以下工具:")
        for tool_call in response_data["tool_calls"]:
            print(f"🔧 {tool_call['name']}")
            print(f"🔧 参数: {json.dumps(tool_call['arguments'], ensure_ascii=False, indent=2)}")
            print(f"🔧 结果: {json.dumps(tool_call['response'], ensure_ascii=False, indent=2)}")
            print("--------------------------------")
    
    # 显示最终回复
    print(f"\n🤖 回复: {response_data['response']}")

def main():
    """
    主函数
    """
    try:
        # 创建聊天机器人实例
        chatbot = Chatbot()
        
        print("🤖欢迎使用聊天机器人！(输入'退出'或'exit'结束对话，输入'清空'或'clear'清除对话历史)")
        print("🔧支持的工具：获取当前时间、执行数学计算、知识库搜索🔧")
        
        while True:
            # 获取用户输入
            user_input = input("\n👤请输入: ")
            
            # 检查退出命令
            if user_input.lower() in ["退出", "exit", "quit", "q"]:
                print("🤖 再见！")
                break
            
            # 检查清空历史命令
            if user_input.lower() in ["清空", "clear", "c"]:
                chatbot.clear_history()
                print("已清空对话历史！")
                continue
            
            # 调用聊天机器人处理输入
            response_data = chatbot.chat(user_input)
            
            # 显示机器人回复
            display_bot_response(response_data)
            
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
        print(f"程序出错: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 