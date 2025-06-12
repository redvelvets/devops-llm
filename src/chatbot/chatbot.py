"""
基于LiteLLM的聊天机器人实现，支持工具调用
"""
import json
from typing import Dict, Any, List

import litellm
from loguru import logger
from src.config.config_loader import get_settings
from src.chatbot.tools import TOOLS, TOOL_FUNCTIONS

settings = get_settings()

class Chatbot:
    def __init__(self, 
                 model: str = None, 
                 api_key: str = None, 
                 api_base: str = None,
                 system_prompt: str = "你是一个有用的AI助手，能够回答问题并使用提供的工具完成任务。"):
        """
        初始化聊天机器人
        
        Args:
            model: 要使用的模型名称
            api_key: API密钥
            api_base: API基础URL
            system_prompt: 系统提示
        """
        # 如果未提供参数，使用配置中的默认值
        self.model = model or settings.litellm_qwen_plus.model
        self.api_key = api_key or settings.litellm_qwen_plus.api_key
        self.api_base = api_base or settings.litellm_qwen_plus.api_base
        
        # 设置LiteLLM参数
        litellm.api_key = self.api_key
        litellm.api_base = self.api_base
        
        # 初始化对话历史
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
    
    def add_message(self, role: str, content: str) -> None:
        """
        添加消息到对话历史
        """
        self.messages.append({"role": role, "content": content})
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """
        获取对话历史
        """
        return self.messages
    
    def clear_history(self) -> None:
        """
        清除对话历史，保留系统提示
        """
        system_prompt = None
        for message in self.messages:
            if message["role"] == "system":
                system_prompt = message["content"]
                break
        
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
    
    def execute_tool(self, tool_call: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行工具调用
        """
        try:
            function_name = tool_call["function"]["name"]
            function_args = json.loads(tool_call["function"]["arguments"])
            
            if function_name in TOOL_FUNCTIONS:
                function_to_call = TOOL_FUNCTIONS[function_name]
                function_response = function_to_call(**function_args)
                return {
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response, ensure_ascii=False)
                }
            else:
                return {
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps({"error": f"未找到工具函数: {function_name}"}, ensure_ascii=False)
                }
        except Exception as e:
            logger.error(f"执行工具时出错: {e}")
            return {
                "tool_call_id": tool_call["id"],
                "role": "tool",
                "name": tool_call["function"]["name"],
                "content": json.dumps({"error": f"执行工具时出错: {str(e)}"}, ensure_ascii=False)
            }
    
    def chat(self, user_input: str) -> Dict[str, Any]:
        """
        处理用户输入并返回响应
        """
        try:
            # 添加用户消息
            self.add_message("user", user_input)
            
            # 调用模型生成回复
            response = litellm.completion(
                model=self.model,
                messages=self.messages,
                tools=TOOLS
            )
            
            # 提取模型回复
            assistant_message = response.choices[0].message
            
            # 处理可能的工具调用
            if assistant_message.tool_calls:
                # 添加助手消息到历史记录
                self.messages.append(assistant_message)
                
                # 处理所有工具调用
                for tool_call in assistant_message.tool_calls:
                    # 执行工具调用
                    tool_response = self.execute_tool(tool_call)
                    # 添加工具响应到历史记录
                    self.messages.append(tool_response)
                
                # 再次调用模型，使其处理工具响应
                second_response = litellm.completion(
                    model=self.model,
                    messages=self.messages
                )
                
                # 提取最终响应
                final_message = second_response.choices[0].message
                self.messages.append(final_message)
                
                return {
                    "response": final_message.content,
                    "tool_calls": [
                        {
                            "name": tool_call["function"]["name"],
                            "arguments": json.loads(tool_call["function"]["arguments"]),
                            "response": json.loads(next(
                                (msg["content"] for msg in self.messages 
                                 if msg.get("tool_call_id") == tool_call["id"]), 
                                "{}"
                            ))
                        } for tool_call in assistant_message.tool_calls
                    ]
                }
            else:
                # 没有工具调用，直接添加助手回复
                self.messages.append(assistant_message)
                return {
                    "response": assistant_message.content,
                    "tool_calls": []
                }
                
        except Exception as e:
            logger.error(f"聊天过程中出错: {e}")
            return {
                "response": f"发生错误: {str(e)}",
                "tool_calls": []
            } 