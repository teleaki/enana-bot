from nonebot.adapters.onebot.v11 import Event, Bot, Message, MessageSegment
import requests
import random
import time  # 用于延迟重试

base_url = "https://storage.sekai.best/sekai-jp-assets/character/member/res{oc_id}_no{oc_num}_rip/{card_type}.png"

oc_dict = {
    'ick': '001', 'saki': '002', 'hnm': '003', 'shiho': '004',
    'mnr': '005', 'hrk': '006', 'airi': '007', 'szk': '008',
    'khn': '009', 'an': '010', 'akt': '011', 'toya': '012',
    'tks': '013', 'emu': '014', 'nene': '015', 'rui': '016',
    'knd': '017', 'mfy': '018', 'ena': '019', 'mzk': '020',
    'miku': '021', 'rin': '022', 'len': '023', 'luka': '024',
    'meiko': '025', 'kaito': '026'
}

oc_num_dict = {
    'ick': 39, 'saki': 43, 'hnm': 42, 'shiho': 44,
    'mnr': 40, 'hrk': 42, 'airi': 41, 'szk': 41,
    'khn': 41, 'an': 41, 'akt': 44, 'toya': 42,
    'tks': 41, 'emu': 42, 'nene': 40, 'rui': 41,
    'knd': 41, 'mfy': 41, 'ena': 42, 'mzk': 40,
    'miku': 52, 'rin': 42, 'len': 44, 'luka': 43, 'meiko': 43, 'kaito': 45
}

card_type = ["card_normal", "card_after_training"]

def url_exists(url):
    """
    检查给定的 URL 是否有效。
    """
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            # 检查返回的内容是否包含 "NoSuchKey" 来判断是否存在该文件
            if "NoSuchKey" in response.text:
                return False  # 文件不存在
            return True  # 图片存在
        elif response.status_code == 403:
            return False  # 可能是权限问题，返回无效
        return False  # 其他状态码认为资源不可用
    except requests.Timeout:
        return False  # 请求超时，无法调用
    except requests.RequestException as e:
        return False  # 请求失败，图片不存在


def get_img(oc_name):
    """
    根据 oc_name 生成一个图片的 URL。
    """
    try:
        # 从配置字典中获取 oc_id 和 oc_num
        oc_id = oc_dict.get(oc_name)
        if not oc_id:
            raise ValueError(f"未找到 {oc_name} 对应的 oc_id")

        # 获取 oc_num 的最大值，生成一个随机的 oc_num
        max_num = oc_num_dict.get(oc_name)
        if max_num is None:
            raise ValueError(f"未找到 {oc_name} 对应的 oc_num")
        ran = random.randint(0, max_num - 1)
        oc_num = f"{ran:03d}"  # 格式化成三位数字

        # 随机选择 card_type
        card_choice = random.choice(card_type)

        # 生成最终的 URL
        url = base_url.format(oc_id=oc_id, oc_num=oc_num, card_type=card_choice)
        return MessageSegment.image(url)

    except Exception as e:
        return MessageSegment.text(f"获取图片失败: {e}")