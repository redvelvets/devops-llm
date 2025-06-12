import litellm
from loguru import logger
from config.config_loader import get_settings

settings = get_settings()

def test_aliyun_llm():
    try:

        # 设置API密钥和基础URL
        litellm.api_key = settings.litellm_qwen_plus.api_key
        litellm.api_base = settings.litellm_qwen_plus.api_base

        # 调用Qwen-Plus模型
        response = litellm.completion(
            model=settings.litellm_qwen_plus.model,
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
