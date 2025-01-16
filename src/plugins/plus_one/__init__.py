from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata, get_loaded_plugins
from nonebot import require

require("nonebot_plugin_session")

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="复读姬",
    description="群内连续出现3次复读会跟随复读",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

# 功能实现
from nonebot.plugin import on_message
from nonebot.adapters import Event, Message, Bot
from nonebot_plugin_session import extract_session, SessionIdType

plus = on_message(
    priority=9,
    block=False)
msg_dict = {}


def is_equal(msg1: Message, msg2: Message):
    """判断是否相等"""
    if len(msg1) == len(msg2) == 1 and msg1[0].type == msg2[0].type == "image":
        if msg1[0].data["file_size"] == msg2[0].data["file_size"]:
            return True
    if msg1 == msg2:
        return True


@plus.handle()
async def plush_handler(bot: Bot, event: Event):
    global msg_dict

    session = extract_session(bot, event)
    group_id = session.get_id(SessionIdType.GROUP).split("_")[-1]

    # 获取群聊记录
    text_list = msg_dict.get(group_id, None)
    if not text_list:
        text_list = []
        msg_dict[group_id] = text_list

    # 获取当前信息
    msg = event.get_message()

    try:
        if not is_equal(text_list[-1], msg):
            text_list = []
            msg_dict[group_id] = text_list
    except IndexError:
        pass

    text_list.append(msg)

    if len(text_list) > 2:
        await plus.send(msg)