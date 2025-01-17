from nonebot.adapters.onebot.v11 import Event, Bot, Message, MessageSegment

from .config import Config

import requests
import random

base_url = "https://storage.sekai.best/sekai-jp-assets/character/member/res{oc_id}_no{oc_num}_rip/{card_type}.png"


def url_exists(url):
    """
    检查给定的 URL 是否有效。
    """
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            # 检查返回的内容是否包含 "NoSuchKey" 来判断是否存在该文件
            if "NoSuchKey" in response.text:
                return False  # 文件不存在
            return True  # 图片存在
        elif response.status_code == 403:
            return False  # 可能是权限问题，返回无效
        return False  # 其他状态码认为资源不可用
    except requests.RequestException as e:
        print(f"请求失败: {e}")  # 输出异常信息，便于调试
        return False  # 请求失败，图片不存在


def get_url(oc_name):
    """
    根据 oc_name 生成一个图片的 URL。
    """
    try:
        # 从配置字典中获取 oc_id 和 oc_num
        oc_id = Config.oc_dict.get(oc_name)
        if not oc_id:
            raise ValueError(f"未找到 {oc_name} 对应的 oc_id")

        # 获取 oc_num 的最大值，生成一个随机的 oc_num
        max_num = Config.oc_num_dict.get(oc_name)
        if max_num is None:
            raise ValueError(f"未找到 {oc_name} 对应的 oc_num")
        ran = random.randint(0, max_num - 1)
        oc_num = f"{ran:03d}"  # 格式化成三位数字

        # 随机选择 card_type
        if not Config.card_type:
            raise ValueError("card_type 列表为空")
        card_type = random.choice(Config.card_type)

        # 生成最终的 URL
        url = base_url.format(oc_id=oc_id, oc_num=oc_num, card_type=card_type)
        return url

    except Exception as e:
        msg = MessageSegment.text(f"获取图片失败: {e}")
        return msg


def get_img(oc_name, max_retries=20):
    """
    获取图片，最多重试 max_retries 次。
    """
    retries = 0
    while retries < max_retries:
        url = get_url(oc_name)
        if isinstance(url, MessageSegment):  # 如果返回的是错误消息
            return url

        if url_exists(url):  # 如果 URL 有效
            return MessageSegment.image(url)

        retries += 1  # 重试次数

    # 如果所有尝试失败，返回失败信息
    return MessageSegment.text("图片获取失败，超过最大重试次数。")
