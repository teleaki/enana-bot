from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="选择",
    description="帮你做选择",
    usage="选择 A还是B",
    config=Config,
)

config = get_plugin_config(Config)

# 功能实现
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Event, Bot, MessageSegment, Message
from nonebot.params import CommandArg
import random

choose = on_command(
    "选择",
    priority=4,
    block=True)

@choose.handle()
async def handle_choose(bot: Bot, event: Event, args: Message = CommandArg()):
    if tmp := args.extract_plain_text():                   # 判断是否有内容
        choices = tmp.split("还是")                         # 切片得到选项
        ran1 = random.randint(0, 100 - 1)
        if ran1 < 10:
            chosen = MessageSegment.text("全都要！")         # 0.1概率下
        else:
            ran2 = random.randint(0, len(choices) - 1)
            chosen = MessageSegment.text(choices[ran2])     # 选择
        msg = Message([
            MessageSegment.reply(id_=event.message_id),
            MessageSegment.text("enana建议你选："),
            chosen
        ])
        await choose.finish(msg)
    else:
        await choose.finish("请输入内容")

