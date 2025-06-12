from openai import OpenAI
from loguru import logger
from config.config_loader import get_settings

settings = get_settings()
def test_aliyun_llm():

    client = OpenAI(
        api_key=settings.openai_qwen_plus.api_key,
        base_url=settings.openai_qwen_plus.api_base,
    )

    completion = client.chat.completions.create(
        model=settings.openai_qwen_plus.model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你是谁？"},
        ],
        # Qwen3模型通过enable_thinking参数控制思考过程（开源版默认True，商业版默认False）
        # 使用Qwen3开源版模型时，若未启用流式输出，请将下行取消注释，否则会报错
        # extra_body={"enable_thinking": False},
    )
    logger.debug(f"OpenAI LLM Reply: \n {completion.choices[0].message.content}")

def main():
    test_aliyun_llm()

if __name__ == "__main__":
    main()

