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
from .lib.maimaidx_user import *
from .lib.maimaidx_table import *
from .lib.maimaidx_guess import *

import re

# init
driver = get_driver()

@driver.on_startup
async def get_data():
    await mai.get_music_list()
    await mai.get_music_alias()

# user setting
user_setting = on_command(
    '用户设置',
    priority=3,
    block=True
)

@user_setting.handle()
async def handle_b50setting(bot: Bot, event: Event, args: Message = CommandArg()):
    if plate_id := args.extract_plain_text():
        qqid = event.get_user_id()
        flag = set_plate_diy(qqid=qqid, plate_id=plate_id)
        if flag == 0:
            msg = Message([
                MessageSegment.text(f'设置成功，'),
                MessageSegment.at(qqid),
                MessageSegment.text(f'的姓名框已被设置为'),
                MessageSegment.image(other_plate_dir / f'UI_Plate_{plate_id}.png')
            ])
            await user_setting.finish(msg)
        elif flag == 1:
            await user_setting.finish('设置失败，可能姓名框不存在，输入“查看姓名框”查询可用姓名框')
        elif flag == 2:
            await user_setting.finish('已清除设置')
        else:
            await user_setting.finish('设置失败，出错啦！')
    else:
        await user_setting.finish('请输入文字')

plate_show = on_command(
    '查看姓名框',
    priority=3,
    block=True
)

@plate_show.handle()
async def handle_plateshow(bot: Bot, event: Event, args: Message = CommandArg()):
    msg = MessageSegment.image(show_all_plate())
    await plate_show.finish(msg)

show_diy = on_command(
    '查看用户个性化',
    priority=3,
    block=True
)

@show_diy.handle()
async def handle_showdiy(bot: Bot, event: Event, args: Message = CommandArg()):
    msg = Message()
    with open(user_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if data:
        for key, value in data.items():
            msg.append(MessageSegment.text(f'{key}: {value}'))
        await show_diy.finish(msg)
    else:
        await show_diy.finish('暂无信息')

# b50
b50 = on_command(
    "b50",
    aliases={'比50', '看看b'},
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

# info
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

# table
level_table = on_regex(
    r'^(?P<level>\d+[\+]*)分数列表(?P<page>\d*)$',
    priority=3,
    block=True
)

@level_table.handle()
async def handle_level(bot: Bot, event: Event, args: Tuple[Optional[str], Optional[str]] = RegexStr('level', 'page')):
    print(f"Received message: {event.message}")  # 打印消息内容，查看是否匹配
    print(f"Extracted level: {args[0]}, page: {args[1]}")  # 打印捕获的 level 和 page

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
    r'^谱师分数列表(?P<page>\d*)\s+(?P<charter>.+)$',
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

bpm_table = on_regex(
    r'^bpm分数列表(?P<page>\d*)\s+(?P<bpm_min>\d+)-(?P<bpm_max>\d+)$',
    priority=3,
    block=True
)

@bpm_table.handle()
async def handle_charter(bot: Bot, event: Event, args: Tuple[Optional[str], Optional[str], Optional[str]] = RegexStr('bpm_min', 'bpm_max', 'page')):
    print(f"Received message: {event.message}")  # 打印消息内容，查看是否匹配
    print(f"Extracted bpm: {args[0]}-{args[1]}, page: {args[2]}")  # 打印捕获的 bpm 和 page

    bpm_min = int(args[0]); bpm_max = int(args[1])
    page = args[2]
    qqid = event.user_id

    # 这里确保 page 的值合法，避免错误
    if page == 0 or bpm_min > bpm_max:
        await bpm_table.finish("蓝的盆")

    if not page:
        page = 1  # 默认第一页，如果没有传入 page 参数

    page = int(page)  # 确保 page 是整数类型

    bpm_msg = await generate_bpm_table(bpm_min=bpm_min, bpm_max=bpm_max, qqid=qqid, page=page)

    await bpm_table.finish(bpm_msg)

# guess
mai_guess = on_command(
    "mai猜歌",
    aliases={'猜你mai'},
    priority=3,
    block=True
)

@mai_guess.handle()
async def handle_mguess(bot: Bot, matcher: Matcher, event: Event):
    groupid = get_group_id(event)
    print(groupid)

    if groupid in games:
        await mai_guess.finish('已有猜歌游戏正在进行中')

    game = add_game(groupid)

    flag, msg = game.guess_music_start()
    if flag:
        if msg:  # 检查消息是否成功生成
            await mai_guess.send(msg)
            game.timer_task = asyncio.create_task(game.start_timer(matcher, groupid))
        else:
            game.guess_music_end()
            end_game(groupid)
            await mai_guess.finish("游戏启动失败，请稍后再试。")
    else:
        game.guess_music_end()
        end_game(groupid)
        await mai_guess.finish(msg)

mai_guess_answer = on_regex(
    r'^(猜(.*)|不玩了)$',
    priority=4,
    block=True
)

@mai_guess_answer.handle()
async def gc_answer(bot: Bot, event: Event):
    groupid = get_group_id(event)
    if is_started(groupid):
        game = games[groupid]
        cmd = event.get_message().extract_plain_text().strip()
        if cmd == '不玩了':
            msg = game.guess_music_timeout()
            game.guess_music_end()
            end_game(groupid)
            await mai_guess_answer.finish(msg)
        elif cmd.startswith('猜'):
            key = cmd[1:].strip().lower()
            qqid = event.get_user_id()
            flag, msg = game.guess_card_judge(key, qqid=qqid)
            if flag:
                game.guess_music_end()
                end_game(groupid)
                await mai_guess_answer.finish(msg)
            else:
                await mai_guess_answer.send(msg)