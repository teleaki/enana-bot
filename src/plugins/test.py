from nonebot import on_regex
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message

from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="测试",
    description="查看bot是否启动成功",
    usage="测试",
)

Test =on_regex(
    pattern=r'^测试$',
    priority=1,
    block=True
)

@Test.handle()
async def Test_send(bot:Bot,event:GroupMessageEvent,state:T_State):
    msg ="Bot启动成功"
    await Test.finish(message=Message(msg))