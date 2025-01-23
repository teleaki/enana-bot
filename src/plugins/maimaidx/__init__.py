from nonebot import get_plugin_config, get_driver
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="maimaidx",
    description="舞萌dx相关工具",
    usage="b50",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot import on_command, on_regex
from nonebot.adapters.onebot.v11 import Bot, Message, Event
from nonebot.params import CommandArg

from .lib.maimaidx_best50 import *


driver = get_driver()

@driver.on_startup
async def get_data():
    await mai.get_music_list()
    await mai.get_music_alias()


b50 = on_command(
    "b50",
    aliases={'比50'},
    priority=3,
    block=True
)

@b50.handle()
async def handle_b50(bot: Bot, event: Event, args: Message = CommandArg()):
    if username := args.extract_plain_text():
        b50_msg = await generate_b50(username=username)
    else:
        qqid = event.user_id
        b50_msg = await generate_b50(qqid=qqid)

    await b50.finish(Message(b50_msg))