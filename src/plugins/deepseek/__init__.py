from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="deepseek",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, Event
from nonebot.params import CommandArg

from .deepseek import *


# 命令处理器
deepseek = on_command(
    'ena',
    aliases={'enai'},
    priority=8,
    block=True
)


@deepseek.handle()
async def handle_deepseek(
        bot: Bot,
        event: Event,
        state: T_State,
        args: Message = CommandArg()
):
    user_id = event.get_user_id()
    question = args.extract_plain_text().strip()

    if not question:
        await deepseek.finish("请输入您的问题")

    # 显示等待提示
    await bot.send(event, "正在思考中...")

    # 获取客户端实例
    client = await init_async_client()

    try:
        # 带超时的请求
        reply = await asyncio.wait_for(
            safe_async_chat(client, user_id, question),
            timeout=300.0
        )

        # 发送最终回复
        await deepseek.send(reply)

    except asyncio.TimeoutError:
        await deepseek.finish("思考超时，请尝试简化您的问题")

    except Exception as e:
        await deepseek.finish(f"服务暂时不可用，错误信息：{str(e)[:50]}")