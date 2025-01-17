from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="看烤的卡面",
    description="发送指定角色的随机卡面",
    usage="看xxx",
    config=Config,
)

config = get_plugin_config(Config)

# 功能实现
from nonebot import on_regex
from nonebot.adapters.onebot.v11 import Event, Bot, Message, MessageSegment

from .get_img import get_img

seekai = on_regex(
    r"看(ick|saki|hnm|shiho|"
    r"mnr|hrk|airi|szk|"
    r"khn|an|akt|toya|"
    r"tks|emu|nene|rui|"
    r"knd|mfy|ena|mzk|"
    r"miku|rin|len|luka|meiko|kaito)",
    priority=5,
    block=True
)

@seekai.handle()
async def handle_seekai(event: Event):
    oc_name = event.regex.group(1)
    msg = get_img(oc_name)
    await seekai.finish(msg)
