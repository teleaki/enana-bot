from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata, get_loaded_plugins

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="帮助",
    description="列出所有功能",
    usage="帮助",
    config=Config,
)

config = get_plugin_config(Config)

# 功能实现
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message
from nonebot.typing import T_State

# 创建一个命令处理器，响应用户输入的"帮助"命令
Help = on_command(
    "帮助",
    priority=5,
    block=True,
)


# 定义命令的回调函数
@Help.handle()
async def handle_help(bot: Bot, event: GroupMessageEvent, state: T_State):

    loaded_plugins = get_loaded_plugins()

    # 创建功能列表，列出所有插件的名称和命令
    function_list = []
    for plugin in loaded_plugins:
        if isinstance(plugin.metadata, PluginMetadata):
            # 插件的元数据（包括插件名称和描述）
            plugin_name = plugin.metadata.name or "未知插件"
            plugin_desc = plugin.metadata.description or "无描述"
            plugin_usage = plugin.metadata.usage or "无使用方法"
        else:
            plugin_name = plugin.name or "未知插件"
            plugin_desc = "无描述"
            plugin_usage = "无使用方法"

        # # 获取该插件注册的所有命令
        # for command in plugin.matcher:
        #     command_name = command.__name__

        # TODO: command name获取失败，暂时先不打印command name，默认插件名与command name一致
        function_list.append(f"{plugin_name}: {plugin_desc}\nusage: {plugin_usage}\n")

    # bot信息
    enana_info = "欢迎使用enana-bot v0.1 \n"
    haruki_info = "haruki-cli: pjsk相关功能\nusage: 详情见 https://docs.haruki.seiunx.com \n"
    # 如果没有注册的命令，提示没有功能
    help_message = "目前支持的功能有：\n\n" + haruki_info + "\n".join(function_list)

    await bot.send(event, enana_info + help_message)