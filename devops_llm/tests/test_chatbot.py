"""
聊天机器人测试文件
"""
from loguru import logger
from chatbot import Chatbot

def test_basic_chat():
    """
    测试基本的聊天功能
    """
    try:
        # 创建聊天机器人实例
        chatbot = Chatbot()
        
        # 测试简单问答
        response = chatbot.chat("你好，请介绍一下自己")
        logger.info(f"回复: {response['response']}")
        
        # 测试连续对话
        response = chatbot.chat("你能做什么？")
        logger.info(f"回复: {response['response']}")
        
        print("基本聊天测试完成")
    except Exception as e:
        logger.error(f"测试基本聊天功能时出错: {e}")

def test_tool_calling():
    """
    测试工具调用功能
    """
    try:
        # 创建聊天机器人实例
        chatbot = Chatbot()
        
        # 测试时间工具
        response = chatbot.chat("现在几点了？")
        logger.info(f"回复: {response['response']}")
        if response["tool_calls"]:
            logger.info(f"工具调用: {response['tool_calls']}")
        
        # 测试计算工具
        response = chatbot.chat("计算23乘以45等于多少？")
        logger.info(f"回复: {response['response']}")
        if response["tool_calls"]:
            logger.info(f"工具调用: {response['tool_calls']}")
        
        # 测试知识库搜索工具
        response = chatbot.chat("Python是什么？")
        logger.info(f"回复: {response['response']}")
        if response["tool_calls"]:
            logger.info(f"工具调用: {response['tool_calls']}")
        
        print("工具调用测试完成")
    except Exception as e:
        logger.error(f"测试工具调用功能时出错: {e}")

def main():
    """
    主函数
    """
    print("开始测试聊天机器人")
    
    # 测试基本聊天功能
    test_basic_chat()
    
    # 测试工具调用功能
    test_tool_calling()
    
    print("所有测试完成")

if __name__ == "__main__":
    main() 