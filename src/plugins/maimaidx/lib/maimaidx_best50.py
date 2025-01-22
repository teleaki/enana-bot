from nonebot.adapters.onebot.v11 import MessageSegment, Bot, Message
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Union
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import math, base64

from .maimaidx_api import maiapi
from .maimaidx_error import *
from .maimaidx_model import *


class DrawBest:
    def __init__(self, user_info: UserInfo, qqid: Optional[Union[int, str]] = None):
        self.nickname = user_info.nickname
        self.plate = user_info.plate
        self.addRating = user_info.additional_rating
        self.Rating = user_info.rating
        self.sdBest = user_info.charts.sd
        self.dxBest = user_info.charts.dx
        self.qqid = qqid

    def draw(self) -> Image.Image:
        img = Image.new('RGB', (1760, 2000), color='white')
        draw = ImageDraw.Draw(img)
        font_path : Path = Path(__file__).parent.parent / 'msyh.ttf'
        font = ImageFont.truetype(font_path, size=15)

        # 用户信息
        head_texts = [
            f'nickname: {self.nickname}',
            f'plate: {self.plate}',
            f'Rating: {self.Rating}',
        ]
        y = 30
        for head_text in head_texts:
            bbox = draw.textbbox((0, 0), head_text, font=font)
            text_width = bbox[2] - bbox[0]  # 右边界 - 左边界
            text_height = bbox[3] - bbox[1]  # 下边界 - 上边界

            draw.text((10, y), head_text, font=font, fill="black")

            y += text_height + 10

        # b35信息
        b35_texts = []
        for _m in self.sdBest:
            b35_texts.append(f'id{_m.song_id}: {_m.title}({_m.type}) [{_m.level_label}]{_m.ds}\n'
                             f'{_m.achievements:.4f}')
        y = 150
        draw.text((10, y), 'b35:', font=font, fill="black")
        y = 180
        for b35_text in b35_texts:
            bbox = draw.textbbox((0, 0), b35_text, font=font)
            text_width = bbox[2] - bbox[0]  # 右边界 - 左边界
            text_height = bbox[3] - bbox[1]  # 下边界 - 上边界

            draw.text((10, y), b35_text, font=font, fill="black")

            y += text_height + 10

        # b15信息
        b15_texts = []
        for _m in self.dxBest:
            b15_texts.append(f'id{_m.song_id}: {_m.title}({_m.type}) [{_m.level_label}]{_m.ds}\n'
                             f'{_m.achievements:.4f}')
        y = 1300
        draw.text((10, y), 'b15:', font=font, fill="black")
        y = 1330
        for b15_text in b15_texts:
            bbox = draw.textbbox((0, 0), b15_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            draw.text((10, y), b15_text, font=font, fill="black")

            y += text_height + 10

        return img

def compute_ra(ds: float, achievement: float) -> int:
    base_ra = 22.4
    if achievement < 50:
        base_ra = 7.0
    elif achievement < 60:
        base_ra = 8.0
    elif achievement < 70:
        base_ra = 9.6
    elif achievement < 75:
        base_ra = 11.2
    elif achievement < 80:
        base_ra = 12.0
    elif achievement < 90:
        base_ra = 13.6
    elif achievement < 94:
        base_ra = 15.2
    elif achievement < 97:
        base_ra = 16.8
    elif achievement < 98:
        base_ra = 20.0
    elif achievement < 99:
        base_ra = 20.3
    elif achievement < 99.5:
        base_ra = 20.8
    elif achievement < 100:
        base_ra = 21.1
    elif achievement < 100.5:
        base_ra = 21.6

    return math.floor(ds * (min(100.5, achievement) / 100) * base_ra)

def image_to_base64(img: Image.Image, format='PNG') -> str:
    output_buffer = BytesIO()
    img.save(output_buffer, format)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode()
    return 'base64://' + base64_str

async def generate_b50(qqid: Optional[int] = None, username: Optional[str] = None) -> MessageSegment:
    try:
        if username:
            qqid = None
        obj = await maiapi.query_user('player', qqid=qqid, username=username)

        user_info = UserInfo(**obj)
        draw_best = DrawBest(user_info = user_info, qqid = qqid)

        pic = draw_best.draw()
        msg = MessageSegment.image(image_to_base64(pic))
    except UserNotFoundError as e:
        msg = MessageSegment.text(str(e))
    except UserDisabledQueryError as e:
        msg = MessageSegment.text(str(e))
    except OSError as e:
        msg = MessageSegment.text(f"Error occurred: {e}")
    except Exception as e:
        msg = MessageSegment.text(f'未知错误：{type(e)}\n请联系Bot管理员')
    return msg