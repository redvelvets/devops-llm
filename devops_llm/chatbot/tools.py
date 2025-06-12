"""
定义可以被聊天机器人调用的工具函数
"""
from typing import Dict, Any, List, Optional
from datetime import datetime


def get_current_time() -> Dict[str, Any]:
    """
    获取当前时间
    """
    current_time = datetime.now()
    return {
        "year": current_time.year,
        "month": current_time.month,
        "day": current_time.day,
        "hour": current_time.hour,
        "minute": current_time.minute,
        "second": current_time.second,
        "formatted": current_time.strftime("%Y-%m-%d %H:%M:%S")
    }


def calculate(operation: str, x: float, y: float) -> Dict[str, Any]:
    """
    执行简单的算术运算
    """
    result = None
    if operation == "add":
        result = x + y
    elif operation == "subtract":
        result = x - y
    elif operation == "multiply":
        result = x * y
    elif operation == "divide":
        if y == 0:
            return {"error": "除数不能为零"}
        result = x / y
    else:
        return {"error": f"不支持的运算: {operation}"}
    
    return {"result": result}


def search_knowledge_base(query: str) -> Dict[str, Any]:
    """
    模拟知识库搜索功能
    """
    # 实际应用中，这里可以连接到真实的知识库或向量数据库
    knowledge = {
        "python": "Python是一种高级编程语言，以其简洁易读的语法著称。",
        "devops": "DevOps是一组实践，旨在缩短开发周期并提供高质量软件交付。",
        "llm": "LLM（大型语言模型）是一种基于深度学习的AI模型，能够理解和生成人类语言。",
        "chatbot": "聊天机器人是一种使用AI技术与人类进行对话的应用程序。"
    }
    
    for key, value in knowledge.items():
        if key.lower() in query.lower():
            return {"result": value}
    
    return {"result": "没有找到相关信息"}


# 工具函数配置
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前系统时间",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "要执行的数学运算类型"
                    },
                    "x": {
                        "type": "number",
                        "description": "第一个数值"
                    },
                    "y": {
                        "type": "number",
                        "description": "第二个数值"
                    }
                },
                "required": ["operation", "x", "y"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "在知识库中搜索信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索查询"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# 工具函数字典，用于查找和执行工具
TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "search_knowledge_base": search_knowledge_base
} 