from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="吃/喝什么",
    description="帮你决定吃/喝什么",
    usage="(早上|中午|晚上|夜宵|) (吃|喝)什么，",
    config=Config,
)

config = get_plugin_config(Config)

# 功能实现
from nonebot import on_regex, on_command

from .get_resource import eord_manager
from .menu_manage import menu_show

what2eat = on_regex(
    r"^(早上|中午|晚上|夜宵|)吃什么$",
    priority=5,
    block=True
)

what2drink = on_regex(
    r"^(早上|中午|晚上|半夜|)喝什么$",
    priority=5,
    block=True
)

menu = on_command(
    ("菜单", "查看"),
    priority=5,
    block=True
)

@what2eat.handle()
async def handle_w2e():
    food_msg = eord_manager.get_food()
    await what2eat.finish(food_msg)

@what2drink.handle()
async def handle_w2d():
    drink_msg = eord_manager.get_drink()
    await what2drink.finish(drink_msg)

@menu.handle()
async def handle_menu():
    menu_msg = menu_show()
    await menu.finish(menu_msg)