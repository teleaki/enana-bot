from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="吃/喝什么",
    description="帮你决定吃/喝什么",
    usage="(早上|中午|晚上|夜宵|) (吃|喝)什么，",
    config=Config,
)

config = get_plugin_config(Config)

# 功能实现
from nonebot import on_regex, on_command
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent, PrivateMessageEvent

from .get_resource import eord_manager
from .menu_manage import menu_show

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

what2eat = on_regex(
    r"^(早上|中午|晚上|夜宵|)吃什么$",
    priority=5,
    block=True
)

what2drink = on_regex(
    r"^(早上|中午|晚上|半夜|)喝什么$",
    priority=5,
    block=True
)

menu = on_command(
    ("菜单", "查看"),
    priority=5,
    block=True
)

@what2eat.handle()
async def handle_w2e():
    food_msg = eord_manager.get_food()
    await what2eat.finish(food_msg)

@what2drink.handle()
async def handle_w2d():
    drink_msg = eord_manager.get_drink()
    await what2drink.finish(drink_msg)

@menu.handle()
async def handle_menu(bot: Bot, event: MessageEvent):
    menu_msgs = menu_show()
    bot_id, bot_name = bot.get_login_info()
    await send_forward_msg(bot=bot, event=event, name=bot_name, uin=bot_id, msgs=menu_msgs)