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
from nonebot.params import CommandArg, RegexStr

from .lib.maimaidx_best50 import *
from .lib.maimaidx_info import *
from .lib.maimaidx_table import *

import re

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
        qqid = event.get_user_id()
        b50_msg = await generate_b50(qqid=int(qqid))
        print(qqid)

    await b50.finish(Message(b50_msg))

minfo = on_command(
    "查歌",
    aliases={'id', 'm查歌'},
    priority=3,
    block=True
)

@minfo.handle()
async def handle_minfo(bot: Bot, event: Event, args: Message = CommandArg()):
    if tar := args.extract_plain_text():
        minfo_msg = search_song(tar)
    else:
        minfo_msg = Message('请输入内容')

    await minfo.finish(minfo_msg)

level_table = on_regex(
    r'^(?P<level>\d+[\+]*)分数列表(?P<page>\d*)$',
    priority=3,
    block=True
)

@level_table.handle()
async def handle_level(bot: Bot, event: Event, args: Tuple[Optional[str], Optional[str]] = RegexStr('level', 'page')):
    # print(f"Received message: {event.message}")  # 打印消息内容，查看是否匹配
    # print(f"Extracted level: {args[0]}, page: {args[1]}")  # 打印捕获的 level 和 page

    level = args[0]
    page = args[1]
    qqid = event.user_id

    # 这里确保 level 和 page 的值合法，避免错误
    if level not in levelList or page == 0:
        await level_table.finish("蓝的盆")

    if not page:
        page = 1  # 默认第一页，如果没有传入 page 参数

    page = int(page)  # 确保 page 是整数类型

    level_msg = await generate_level_table(level=level, qqid=qqid, page=page)

    await level_table.finish(level_msg)

charter_table = on_regex(
    r'^(?P<charter>.+)分数列表(?P<page>\d*)$',
    priority=3,
    block=True
)

@charter_table.handle()
async def handle_charter(bot: Bot, event: Event, args: Tuple[Optional[str], Optional[str]] = RegexStr('charter', 'page')):
    print(f"Received message: {event.message}")  # 打印消息内容，查看是否匹配
    print(f"Extracted charter: {args[0]}, page: {args[1]}")  # 打印捕获的 charter 和 page

    charter = args[0]
    page = args[1]
    qqid = event.user_id

    # 这里确保 page 的值合法，避免错误
    if page == 0 or not charter:
        await charter_table.finish("蓝的盆")

    if not page:
        page = 1  # 默认第一页，如果没有传入 page 参数

    page = int(page)  # 确保 page 是整数类型

    charter_msg = await generate_charter_table(charter=charter, qqid=qqid, page=page)

    await charter_table.finish(charter_msg)