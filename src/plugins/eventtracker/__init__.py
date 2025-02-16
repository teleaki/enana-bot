from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="pjsk活动提醒",
    description="结活提醒以及当前活动查询",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment
from .event_tracker import get_event_info

event_info = on_command(
    '查询当前活动',
    priority=5,
    block=True
)

@event_info.handle()
async def event_info():
    await event_info.finish(get_event_info())