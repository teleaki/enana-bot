from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="复读姬",
    description="群内连续出现3次复读会跟随复读",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

# 功能实现
from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message

plus = on_message(
    priority=10,
    block=False
)
msg_dict = {}

def is_equal(msg1: Message, msg2: Message):
    """判断消息是否相等"""
    if len(msg1) == len(msg2) == 1 and msg1[0].type == msg2[0].type == "image":
        if msg1[0].data["file_size"] == msg2[0].data["file_size"]:
            return True
    if msg1 == msg2:
        return True

@plus.handle()
async def plush_handler(bot: Bot, event: GroupMessageEvent):
    global msg_dict

    group_id = event.group_id

    # 获取群聊记录
    text_list = msg_dict.get(group_id, None)
    if not text_list:
        text_list = []
        msg_dict[group_id] = text_list

    # 获取当前消息
    msg = event.get_message()

    try:
        # 如果当前消息与上一条消息不相等，则清空历史消息
        if not is_equal(text_list[-1]["message"], msg):
            text_list = []  # 如果不同，清空历史
            msg_dict[group_id] = text_list
    except IndexError:
        pass

    # 添加当前消息
    text_list.append({"message": msg, "timestamp": event.timestamp})

    # 检查是否有三条连续相同的消息
    if len(text_list) >= 3:
        # 如果最近三条消息都相同，则执行操作
        if is_equal(text_list[-1]["message"], text_list[-2]["message"]) and is_equal(text_list[-2]["message"], text_list[-3]["message"]):
            # 发送重复消息或做其他操作
            await plus.send(msg)
            # 处理后清空历史记录，防止消息再次触发
            text_list.clear()
        else:
            # 如果没有三条相同消息，保留历史
            text_list = text_list[-2:]  # 保留最后两条消息
            msg_dict[group_id] = text_list