from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="pjsk猜卡面",
    description="60s内通过局部截图猜是谁的卡面",
    usage="pjsk猜卡面",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot import on_command, on_regex
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, Event

from .guess import add_game, end_game, games, start_timer

import asyncio

def get_group_id(event: Event) -> str:
    sessionid = event.get_session_id()
    groupid = sessionid.split('_')[1]
    return groupid

def is_started(groupid: str) -> bool:
    if groupid in games:
        return True
    return False


guess_card = on_command(
    "pjsk猜卡面",
    priority=1,
    block=True
)

@guess_card.handle()
async def gc_handle(matcher: Matcher, bot: Bot, event: Event):
    groupid = get_group_id(event)
    print(groupid)

    if groupid in games:
        await guess_card.finish('已有猜卡面游戏正在进行中')

    game = add_game(groupid)

    msg = game.guess_card_start()
    if msg:  # 检查消息是否成功生成
        await guess_card.send(msg)
        game.timer_task = asyncio.create_task(start_timer(matcher, groupid))
    else:
        await guess_card.finish("游戏启动失败，请稍后再试。")

guess_card_answer = on_regex(
    r'^(猜(\w+)|不玩了)$',
    priority=3,
    block=True
)

@guess_card_answer.handle()
async def gc_answer(bot: Bot, event: Event):
    groupid = get_group_id(event)
    if is_started(groupid):
        game = games[groupid]
        cmd = event.get_message().extract_plain_text().strip()
        if cmd == '不玩了':
            msg = game.guess_card_timeout()
            game.guess_card_end()
            end_game(groupid)
            await guess_card.finish(msg)
        elif cmd.startswith('猜'):
            key = cmd[1:].strip().lower()
            qqid = event.get_user_id()
            flag, msg = game.guess_card_judge(key, qqid=qqid)
            if flag:
                game.guess_card_end()
                end_game(groupid)
                await guess_card.finish(msg)
            else:
                await guess_card.send(msg)

