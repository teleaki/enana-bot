import asyncio
from openai import AsyncOpenAI
from typing import List, Dict, Tuple, Optional


# 按会话隔离的消息历史 (user_id: messages)
message_histories: Dict[str, List[Dict[str, str]]] = {}


# 异步客户端初始化 (推荐在驱动器中初始化)
async def init_async_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key="ifdu",
        base_url="https://mapi.fduer.com/api/v1"
    )


# 带锁的异步聊天函数
async def safe_async_chat(
        client: AsyncOpenAI,
        user_id: str,
        message: str,
        model: str = "deepseek-r1-671b",
        max_history: int = 6
) -> str:
    # 获取或初始化消息历史
    history = message_histories.get(user_id, [])

    # 添加上下文（保留最近 max_history 轮对话）
    history.append({"role": "user", "content": message})
    history = history[-max_history * 2:]  # 保持对话轮次平衡

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=history,
            temperature=0.6,
            max_tokens=1024
        )

        if response.choices and response.choices[0].message.content:
            reply = response.choices[0].message.content
            history.append({"role": "assistant", "content": reply})
            message_histories[user_id] = history
            return reply

    except Exception as e:
        message_histories.pop(user_id, None)  # 清除错误会话
        return f"请求失败，请稍后再试（错误代码：{str(e)[:30]}）"

def split_reply(text: str) -> Tuple[str, str]:
    # 分割出思考内容
    think_start = text.find("<think>") + len("<think>")
    think_end = text.find("</think>")
    think_content = text[think_start:think_end]

    # 分割出回答内容
    answer_content = text[think_end + len("</think>"):]

    return think_content, answer_content

def clear_history(user_id: str) -> bool:
    if user_id in message_histories:
        del message_histories[user_id]
        return True
    return False