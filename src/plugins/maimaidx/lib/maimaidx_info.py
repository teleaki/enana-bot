from difflib import SequenceMatcher

from nonebot.adapters.onebot.v11 import Event, Message, MessageSegment

from .maimaidx_music import mai, get_music_cover
from .maimaidx_api import maiapi
from .maimaidx_model import *
from .maimaidx_image import *
from .maimaidx_error import *
from .maimaidx_res import *


# 比较相似度
def is_similar(input_string, string_list, threshold=0.6):
    for string in string_list:
        similarity = SequenceMatcher(None, input_string, string).ratio()
        if similarity > threshold:
            return True
    return False

def song_info_tamp(music: Music) -> Message:
    cover = get_music_cover(music.id)
    ds_info = '/'.join(map(str, music.ds))
    fit_ds_info = "/".join([
        f"{item['fit_diff']:.3f}" for item in music.stats if "fit_diff" in item
    ])
    msg = Message([
        f'{music.id}. {music.title} ({music.type})\n',
        MessageSegment.image(image_to_base64(cover)),
        f'艺术家：{music.basic_info.artist}\n',
        f'分类：{music.basic_info.genre}\n',
        f'版本：{music.basic_info.version}\n',
        f'BPM：{music.basic_info.bpm}\n',
        f'定数：{ds_info}\n',
        f'拟合定数：{fit_ds_info}\n'
    ])
    return msg

def send_song(targets: List[Music]) -> Message:
    if len(targets) == 1:
        target = targets[0]
        return song_info_tamp(target)
    elif len(targets) > 1:
        msg = Message(f'检测到多个乐曲，请使用id查询：\n')
        for target in targets:
            msg.append(f'{target.id}. {target.title} ({target.type})\n')
        return msg

def search_song(arg: Union[int, str]) -> Message:
    targets = []

    # 先找id
    for music in mai.total_list:
        if music.id == str(arg):
            targets.append(music)
    if targets:
        msg = send_song(targets)
        return msg

    # 再找曲名
    for music in mai.total_list:
        if music.title == str(arg):
            targets.append(music)
    if targets:
        msg = send_song(targets)
        return msg

    # 再找别名
    for music in mai.total_alias_list:
        if is_similar(str(arg), music.aliases):
            targets.append(mai.total_list.search_by_id(music.id))

    if targets:
        msg = send_song(targets)
        return msg

    msg = Message(f'未找到该歌曲')
    return msg
