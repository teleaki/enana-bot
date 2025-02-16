import httpx
from typing import Optional, Dict, Any, Union
import datetime
from zoneinfo import ZoneInfo
from nonebot.adapters.onebot.v11 import Message, MessageSegment


def get_current_event() -> Optional[Dict[str, Any]]:
    """
    获取当前活动原始数据（保持API返回的原始结构）

    Returns:
        dict: 原始JSON数据，失败时返回None
    """
    url = "https://strapi.sekai.best/sekai-current-event"

    try:
        with httpx.Client(
                timeout=10.0,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip, deflate"
                }
        ) as client:
            # 发送请求并验证状态码
            response = client.get(url)
            response.raise_for_status()

            # 直接返回原始JSON数据
            return response.json()

    except httpx.HTTPStatusError as e:
        print(f"[错误] HTTP状态异常: {e.response.status_code}")
        if e.response.status_code == 404:
            print("提示：接口地址可能已变更，请检查URL有效性")
    except httpx.RequestError as e:
        print(f"[错误] 网络请求失败: {str(e)}")
        print("建议：检查网络连接或重试")
    except ValueError as e:
        print(f"[错误] JSON解析失败: {str(e)}")
        print(f"原始响应内容: {response.text[:200]}...")  # 打印部分响应内容辅助调试

    return None


def time_transform(
        tick: Union[int, float, str],
        target_tz: str = "Asia/Shanghai",
        output_format: Optional[str] = None
) -> Union[datetime.datetime, str]:
    """
    将毫秒级时间戳转换为指定时区的日期时间

    :param tick: 时间戳（支持整数、浮点数字符串）
    :param target_tz: 目标时区（默认上海时区）
    :param output_format: 返回字符串格式，None时返回datetime对象
    :return: 时区敏感的datetime对象或格式化字符串
    """
    # 输入类型处理
    try:
        # 转换字符串类型的数字
        if isinstance(tick, str):
            if not tick.strip().isdigit():
                raise ValueError("非数字字符串")
            tick = int(tick)
    except (TypeError, ValueError) as e:
        raise ValueError(f"无效的时间戳输入: {tick}") from e

    # 时间戳范围检查（1970-2100）
    if not (-31536000000 < tick < 4102444800000):  # 1969-01-01 ~ 2100-01-01
        raise ValueError(f"时间戳超出合理范围: {tick}")

    try:
        # 转换为UTC时间（兼容不同Python版本）
        utc_timestamp = tick / 1000
        utc_dt = datetime.datetime.fromtimestamp(utc_timestamp, datetime.timezone.utc)

        # 时区转换
        target_zone = ZoneInfo(target_tz)
        local_dt = utc_dt.astimezone(target_zone)

        # 格式化输出
        return local_dt.strftime(output_format) if output_format else local_dt

    except OverflowError as e:
        raise ValueError(f"时间戳转换溢出: {tick}") from e
    except Exception as e:
        raise RuntimeError(f"时间转换失败: {str(e)}") from e


def get_event_info() -> Optional[Message]:
    """
    获取当前活动信息并生成格式化消息

    Returns:
        str: 格式化后的活动信息，失败时返回None
    """
    # 获取原始数据
    try:
        event_data = get_current_event()
        if not event_data:
            print("警告: 未获取到活动数据")
            return None

        current_event = event_data.get("eventJson")
        if not current_event:
            print("警告: 活动数据缺少eventJson字段")
            return None

    except Exception as e:
        print(f"数据获取异常: {str(e)}")
        return None

    # 安全提取字段
    event_id = current_event.get("id", "N/A")
    event_name = current_event.get("name", "未知活动")

    # 时间处理
    time_format = "%Y/%m/%d %H:%M:%S"
    time_fields = {
        "startAt": current_event.get("startAt"),
        "aggregateAt": current_event.get("aggregateAt")
    }

    # 转换时间并处理异常
    formatted_times = {}
    for field, timestamp in time_fields.items():
        try:
            if timestamp is None:
                raise ValueError("时间戳为空")
            formatted_times[field] = time_transform(timestamp, output_format=time_format)
        except Exception as e:
            print(f"时间转换错误 ({field}): {str(e)}")
            formatted_times[field] = "时间数据异常"

    # 获取活动logo
    logo_url = f"https://storage.sekai.best/sekai-jp-assets/event/{current_event['assetbundleName']}/logo_rip/logo.webp"

    # 构建消息
    msg = Message([
        MessageSegment.text("当前活动信息：\n"),
        MessageSegment.text(f"ID: {event_id}\n"),
        MessageSegment.text(f"名称: {event_name}\n"),
        MessageSegment.image(logo_url),
        MessageSegment.text(f"开始时间: {formatted_times['startAt']}\n"),
        MessageSegment.text(f"结束时间: {formatted_times['aggregateAt']}"),
    ])

    return msg
