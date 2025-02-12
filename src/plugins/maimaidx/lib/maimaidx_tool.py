import base64
import json
import random
from io import BytesIO
from typing import Union, Any, Optional

import aiofiles
from PIL import Image

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