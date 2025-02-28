from nonebot import get_plugin_config, get_bot
from nonebot.plugin import PluginMetadata
from nonebot import require

require("nonebot_plugin_apscheduler")

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="pjsk活动提醒",
    description="结活提醒以及当前活动查询",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment
from nonebot import logger

from nonebot_plugin_apscheduler import scheduler

from .event_tracker import get_event_info, event_end_notice

@scheduler.scheduled_job("cron", hour="*", minute=0, second=0, id="hourly_task")
async def hourly_task():
    # 获取事件状态
    flag, notice = event_end_notice()

    # 获取机器人实例
    bot = get_bot()

    # 仅当状态码为 0（1小时内结束）时发送消息
    if flag == 0:
        try:
            # 发送群消息
            for group in config.eventtracker.white_list:
                await bot.send_group_msg(group_id=group, message=notice)

            # 发送日志
            logger.success(f"已发送提醒")

        except Exception as e:
            logger.error(f"消息发送失败：{str(e)}")
    else:
        # await bot.send_group_msg(group_id=white_group[0], message=notice)
        logger.info(notice)

event_info = on_command(
    '查询当前活动',
    priority=5,
    block=True
)

@event_info.handle()
async def handle_eventinfo():
    await event_info.finish(get_event_info())

event_notice = on_command(
    '结活提醒',
    priority=8,
    block=True
)

@event_notice.handle()
async def handle_eventnotice():
    flag, notice = event_end_notice()

    for group in config.eventtracker.white_list:
        await event_notice.finish(notice)