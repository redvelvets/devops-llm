import litellm
from loguru import logger

def test_aliyun_llm():
    try:
        # 设置API密钥和基础URL
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        litellm.api_key = "<your-ailiyun-bailian-token>"
        litellm.api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"

        # 调用Qwen-Plus模型
        response = litellm.completion(
            model="openai/qwen-plus",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "你是谁？"},
            ],
        )

        # 记录回复
        logger.debug(f"LiteLLM Reply: \n {response.choices[0].message.content}")

    except Exception as e:
        logger.error(f"Error occurred: {e}")

def main():
    test_aliyun_llm()

if __name__ == "__main__":
    main()
