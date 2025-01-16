from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="setu",
    description="随机涩图",
    usage="setu",
    config=Config,
)

config = get_plugin_config(Config)

# 功能实现
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Event, Bot, MessageSegment
from nonebot.typing import T_State
import httpx, json

setu = on_command(
    "setu",
    priority=4,
    block=True,
)

@setu.handle()
async def setu_handle(bot: Bot, event: Event, state: T_State):
    img = await get_img()   # 获取图片
    await setu.finish(MessageSegment.image(img))    # 发送图片

async def get_img():
    url = "https://www.dmoe.cc/random.php?return=json"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        get_dic = json.loads(resp.text)
    data = get_dic["imgurl"]
    return data