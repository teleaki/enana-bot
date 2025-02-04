import asyncio
from io import BytesIO
from typing import Optional, Union, List, Dict

from PIL import Image
from nonebot.adapters.onebot.v11 import Message, MessageSegment

from .get_img import get_img_url
from .config import oc_dict, card_type, oc_name

import random, httpx, base64


class GuessCard:
    def __init__(self):
        self.answer = None
        self.image = None

    def guess_card_start(self):
        try:
            # 随机选择卡片
            self.answer = random.choice(list(oc_dict.keys()))

            # 获取图片链接
            flag, url = get_img_url(self.answer)
            if flag == 0:
                # 尝试将 URL 转换为图片
                self.image = url2img(url)
                if self.image:
                    # 生成样本
                    sample = get_sample(self.image)
                    # 构造消息
                    msg = Message([
                        MessageSegment.text('开启pjsk猜卡面\n总共有60s的时间来猜出下面图片为谁的卡面，发送“猜xxx”即可，发送“不玩了”停止游戏'),
                        MessageSegment.image(image2base64(sample))
                    ])
                    return msg
                else:
                    # 图片转换失败的处理
                    return Message([MessageSegment.text('图片加载失败，请稍后再试。')])
            else:
                # 图片链接获取失败的处理
                return Message([MessageSegment.text('未能获取到有效的卡面图片。')])

        except Exception as e:
            # 捕获其他异常
            return Message([MessageSegment.text(f'发生错误：{str(e)}')])

    def guess_card_judge(self, key: Optional[str], qqid: Union[int, str]):
        if key:
            if key in list(oc_dict.keys()):
                if key == self.answer:
                    msg = Message([
                        MessageSegment.text('恭喜'),
                        MessageSegment.at(qqid),
                        MessageSegment.text(f'答对了！是 {oc_name[self.answer]} 哦\n'),
                        MessageSegment.image(image2base64(self.image))
                    ])
                    return True, msg
                else:
                    msg = Message([
                        MessageSegment.text(f'回答错误，不是 {oc_name[key]} 哦')
                    ])
                    return False, msg
            else:
                msg = Message([
                    MessageSegment.text('无法识别答案，请使用罗马字简称哦（e.g. miku）')
                ])
                return False, msg
        else:
            msg = Message([
                MessageSegment.text('请输入文字')
            ])
            return False, msg

    def guess_card_timeout(self):
        msg = Message([
            MessageSegment.text(f'很遗憾，没人能猜对，其实是 {oc_name[self.answer]} 哦\n'),
            MessageSegment.image(image2base64(self.image))
        ])
        return msg

    def guess_card_end(self):
        self.answer = None
        self.image = None

games: Dict[str, GuessCard] = {}


def add_game(groupid: str) -> Union[Message, GuessCard]:
    if groupid in games:
        msg = Message([
            MessageSegment.text('已有猜卡面游戏进行中')
        ])
        return msg

    # 创建一个新的 GuessCard 实例并添加到 games 字典
    games[groupid] = GuessCard()
    return games[groupid]


def end_game(groupid: str):
    """结束并清理指定群组的游戏实例"""
    if groupid in games:
        del games[groupid]  # 从 config.py 中的 games 字典中删除实例


def url2img(url):
    with httpx.Client() as client:
        response = client.get(url)

        # 检查请求是否成功
        if response.status_code == 200:
            # 将响应内容转换为字节流
            image_data = BytesIO(response.content)

            # 使用Pillow打开图片
            image = Image.open(image_data)

            # 返回图片
            return image
        else:
            print(f"Failed to retrieve image. Status code: {response.status_code}")
            return None

def image2base64(img: Image.Image, format='PNG') -> str:
    output_buffer = BytesIO()
    img.save(output_buffer, format)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode()
    return 'base64://' + base64_str

def get_sample(img: Image.Image, sample_width: int = 300, sample_height: int = 300):
    # 获取图片的宽度和高度
    width, height = img.size

    # 生成随机位置 (确保不超出图片边界)
    x = random.randint(0, width - sample_width)
    y = random.randint(0, height - sample_height)

    # 定义裁剪区域 (left, upper, right, lower)
    crop_area = (x, y, x + sample_width, y + sample_height)

    # 裁剪图片
    sample = img.crop(crop_area)

    return sample


