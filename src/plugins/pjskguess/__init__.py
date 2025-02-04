from threading import Event

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

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message, Event, MessageSegment
from nonebot.params import ArgPlainText

from .guess import guessCard

guess_card = on_command(
    "pjsk猜卡面",
    priority=1,
    block=True
)

@guess_card.handle()
async def gc_handle():
    if guessCard.answer:
        await guess_card.finish('猜卡面正在进行中哦')
    else:
        start = guessCard.guess_card_start()
        await guess_card.send(start)

@guess_card.got("key", prompt="请回答，你有60秒时间！")
async def gc_key(
    event: Event,
    key: str = ArgPlainText()
):
    # 用户正常输入时的处理逻辑
    if key.startswith('猜'):
        flag, msg = guessCard.guess_card_judge(key[1:], qqid=event.get_user_id())
        if flag:
            guessCard.guess_card_end()
            await guess_card.finish(msg)
        else:
            await guess_card.reject(msg)
    elif key == '不玩了':
        msg = guessCard.guess_card_timeout()
        guessCard.guess_card_end()
        await guess_card.finish(msg)
    else:
        await guess_card.reject()
