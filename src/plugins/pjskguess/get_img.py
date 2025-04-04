from .config import oc_dict, card_type
import httpx
import random

base_url = "https://storage.sekai.best/sekai-jp-assets/character/member/res{oc_id}_no{oc_num}_rip/{card_type}.png"

# oc_dict = {
#     'ick': '001', 'saki': '002', 'hnm': '003', 'shiho': '004',
#     'mnr': '005', 'hrk': '006', 'airi': '007', 'szk': '008',
#     'khn': '009', 'an': '010', 'akt': '011', 'toya': '012',
#     'tks': '013', 'emu': '014', 'nene': '015', 'rui': '016',
#     'knd': '017', 'mfy': '018', 'ena': '019', 'mzk': '020',
#     'miku': '021', 'rin': '022', 'len': '023', 'luka': '024',
#     'meiko': '025', 'kaito': '026'
# }
# card_type = ["card_normal", "card_after_training"]


def is_url_valid(url):
    try:
        with httpx.Client(http2=True, timeout=2) as client:
            response = client.head(url, follow_redirects=True)
            if response.status_code == 200:
                return True
            # 回退到 GET 请求（仅验证 header）
            # response = client.get(url, follow_redirects=True)
            # return response.status_code == 200
    except httpx.RequestError:
        return False



def get_img_url(oc_name, max_retries=5):
    """
    根据 oc_name 生成一个图片的 URL，若生成的 URL 无效则重新尝试。
    """
    attempt = 0  # 当前尝试次数
    while attempt < max_retries:
        try:
            # 从配置字典中获取 oc_id 和 oc_num
            oc_id = oc_dict.get(oc_name)
            if not oc_id:
                raise ValueError(f"未找到 {oc_name} 对应的 oc_id")

            # 获取 oc_num 的最大值，生成一个随机的 oc_num
            # max_num = oc_num_dict.get(oc_name)
            max_num = 60
            if max_num is None:
                raise ValueError(f"未找到 {oc_name} 对应的 oc_num")
            ran = random.randint(0, max_num - 1)
            oc_num = f"{ran:03d}"  # 格式化成三位数字

            # 随机选择 card_type
            card_choice = random.choice(card_type)

            # 生成最终的 URL
            url = base_url.format(oc_id=oc_id, oc_num=oc_num, card_type=card_choice)

            # 验证生成的 URL 是否有效
            if is_url_valid(url):
                return 0, url
            else:
                attempt += 1
                print(f"第 {attempt} 次尝试失败，重新生成 URL。")
        except ValueError as e:
            # 处理值错误异常
            return 1, f"ValueError: {e}"
        except Exception as e:
            # 捕获其他异常
            return 1, f"获取图片失败: {e}"

    # 如果超过最大重试次数仍然失败，返回错误消息
    return 2, "获取图片超时"