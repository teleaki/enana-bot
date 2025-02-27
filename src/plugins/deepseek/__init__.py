from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="ds大模型",
    description="deepseek大模型聊天",
    usage="ena",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, Event, MessageEvent, PrivateMessageEvent
from nonebot.params import CommandArg

from .deepseek import *


async def send_forward_msg(
        bot: Bot,
        event: MessageEvent,
        name: str,
        uin: str,
        msgs: list[Message]
):
    """
    发送合并转发消息。
    * `bot`: Bot 实例
    * `event`: 消息事件
    * `name`: 呢称
    * `uin`: QQ UID
    * `msgs`: 消息列表
    """

    def to_node(msg: Message):
        return {"type": "node", "data": {"name": name, "uin": uin, "content": msg}}

    messages = [to_node(msg) for msg in msgs]
    is_private = isinstance(event, PrivateMessageEvent)
    if is_private:
        # await bot.call_api(
        #     "send_private_forward_msg", user_id=event.user_id, messages=messages
        # )
        await bot.send_private_forward_msg(user_id=event.user_id, messages=messages)
    else:
        # await bot.call_api(
        #     "send_group_forward_msg", group_id=event.group_id, messages=messages
        # )
        await bot.send_group_forward_msg(group_id=event.group_id, messages=messages)

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
        event: MessageEvent,
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
    bot_identity = await bot.get_login_info()

    try:
        # 带超时的请求
        reply = await asyncio.wait_for(
            safe_async_chat(client, user_id, question),
            timeout=300.0
        )

        # 发送最终回复
        think, answer = split_reply(reply)
        msg = [
            Message([
                MessageSegment.reply(id_=event.message_id),
                MessageSegment.at(user_id=user_id)
            ]),
            MessageSegment.text(f'---已深度思考---\n{think}'),
            MessageSegment.text(f'---正式回复---\n{answer}')
        ]

        await send_forward_msg(
            bot=bot,
            event=event,
            name=bot_identity.get('nickname'),
            uin=bot_identity.get('user_id'),
            msgs=msg
        )

        # await deepseek.send(Message([
        #     MessageSegment.reply(id_=event.message_id),
        #     reply
        # ]))

    except asyncio.TimeoutError:
        await deepseek.finish(Message([
            MessageSegment.reply(id_=event.message_id),
            "思考超时，请尝试简化您的问题"
        ]))

    except Exception as e:
        await deepseek.finish(Message([
            MessageSegment.reply(id_=event.message_id),
            f"服务暂时不可用，错误信息：{str(e)[:50]}"
        ]))

clear = on_command(
    ('ena', '清除历史记录'),
    priority=7,
    block=True
)

@clear.handle()
async def clear_handle(bot: Bot, event: Event, state: T_State):
    user_id = event.get_user_id()
    flag = clear_history(user_id)
    if flag:
        await clear.finish(Message([
            MessageSegment.text('已清除用户'),
            MessageSegment.at(user_id),
            MessageSegment.text('的历史记录')
        ]))
    else:
        await clear.finish(Message([
            MessageSegment.text('用户'),
            MessageSegment.at(user_id),
            MessageSegment.text('目前没有历史记录')
        ]))