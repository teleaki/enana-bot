import base64
import json
import random
import math
from io import BytesIO
from typing import Union, Any, Optional

import aiofiles
from PIL import Image
from nonebot.adapters.onebot.v11 import Event

from .maimaidx_api import maiapi
from .maimaidx_res import *


async def openfile(file: Path) -> Union[dict, list]:
    async with aiofiles.open(file, 'r', encoding='utf-8') as f:
        data = json.loads(await f.read())
    return data


async def writefile(file: Path, data: Any) -> bool:
    async with aiofiles.open(file, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=4))
    return True


def get_music_cover(music_id: Union[str, int]) -> Path:
    cover_path = cover_dir / f'{int(music_id)}.png'
    cover_path_sd = cover_dir / f'{int(music_id) - 10000}.png'
    cover_path_dx = cover_dir / f'{int(music_id) + 10000}.png'
    # 检查文件是否存在，若不存在则使用默认的 0.png
    if cover_path.exists():
        cover = cover_path
    elif cover_path_sd.exists():
        cover = cover_path_sd
    elif cover_path_dx.exists():
        cover = cover_path_dx
    else:
        cover = cover_dir / '0.png' # 使用默认的 0.png
    return cover

def get_group_id(event: Event) -> str:
    sessionid = event.get_session_id()
    groupid = sessionid.split('_')[1]
    return groupid

async def get_QQlogo(qqid: Union[str, int]) -> Image.Image:
    qqlogo = Image.open(BytesIO(await maiapi.qq_logo(qqid)))
    return qqlogo.convert("RGBA")

def image_to_base64(img: Image.Image, format='PNG') -> str:
    output_buffer = BytesIO()
    img.save(output_buffer, format)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode()
    return 'base64://' + base64_str

def get_random_file(folder: Path) -> Optional[Path]:
    # 获取文件夹中的所有文件（排除子文件夹）
    files = [f for f in folder.iterdir() if f.is_file()]

    # 如果文件夹中没有文件，返回 None
    if not files:
        return None

    # 随机选择一个文件
    random_file = random.choice(files)

    return random_file  # 直接返回随机文件的 Path 对象

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

def dxScore(dx: int) -> int:
    """
    返回值为 `Tuple`： `(星星种类，数量)`
    """
    if dx <= 85:
        result = 0
    elif dx <= 90:
        result = 1
    elif dx <= 93:
        result = 2
    elif dx <= 95:
        result = 3
    elif dx <= 97:
        result = 4
    else:
        result = 5
    return result

