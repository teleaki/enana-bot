from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="welcome",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot import on_notice
from nonebot.adapters.onebot.v11 import Bot, Message, GroupIncreaseNoticeEvent

welcome = on_notice(
    priority=10,
    block=False
)

@welcome.handle()
async def welcome(bot: Bot, event: GroupIncreaseNoticeEvent):
    user = event.get_user_id()
    at_ = f"欢迎[CQ:at,qq={user}]!\n"
    msg = at_ + "又有新大佬进群了，群地位-1"
    await welcome.finish(msg)
