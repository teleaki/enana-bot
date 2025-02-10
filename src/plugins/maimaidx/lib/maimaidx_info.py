from difflib import SequenceMatcher

from nonebot.adapters.onebot.v11 import Message, MessageSegment

from .maimaidx_image import *
from .maimaidx_model import *
from .maimaidx_music import mai, get_music_cover
from .maimaidx_res import *


# 比较相似度
def is_similar(input_string, string_list, threshold=0.7):
    for string in string_list:
        similarity = SequenceMatcher(None, input_string, string).ratio()
        if similarity > threshold:
            return True
    return False


def extract_fit_diff_from_music(music: Music) -> str:
    # 如果 stats 为空，则返回空字符串
    if not music.stats:
        return ""
    # 提取所有非空的 fit_diff 值
    fit_diff_values = [
        f"{stats.fit_diff:.3f}" for stats in music.stats if stats and stats.fit_diff is not None
    ]
    # 返回格式化后的字符串，值之间用 "/" 隔开
    return " / ".join(fit_diff_values)

def song_info_tamp(music: Music) -> Message:
    cover = get_music_cover(music.id)
    ds_info = ' / '.join(map(str, music.ds))
    fit_ds_info = extract_fit_diff_from_music(music)
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

def draw_level_info(font, dy, music, level_idx):
    font.draw(280, dy + 30, 30, f'{music.level[level_idx]}({music.ds[level_idx]})', (255, 255, 255, 255), 'mm')
    font.draw(280, dy + 60, 20, f'{music.charts[level_idx].charter}', (255, 255, 255, 255), 'mm')

def draw_stats_info(font, music, dy, level_idx):
    font.draw(480, 835 + dy, 40, f'{music.stats[level_idx].fit_diff:.4f}', (0, 0, 0, 255), 'mm')
    font.draw(665, 835 + dy, 40, f'{sum(music.charts[level_idx].notes)}', (0, 0, 0, 255), 'mm')
    font.draw(835, 835 + dy, 40, f'{music.charts[level_idx].notes[0]}', (0, 0, 0, 255), 'mm')
    font.draw(1015, 835 + dy, 40, f'{music.charts[level_idx].notes[1]}', (0, 0, 0, 255), 'mm')
    font.draw(1185, 835 + dy, 40, f'{music.charts[level_idx].notes[2]}', (0, 0, 0, 255), 'mm')
    if music.type.upper() == 'DX':
        font.draw(1360, 835 + dy, 40, f'{music.charts[level_idx].notes[3]}', (0, 0, 0, 255), 'mm')
        font.draw(1535, 835 + dy, 40, f'{music.charts[level_idx].notes[4]}', (0, 0, 0, 255), 'mm')
    else:
        font.draw(1360, 835 + dy, 40, f'-', (0, 0, 0, 255), 'mm')
        font.draw(1535, 835 + dy, 40, f'{music.charts[level_idx].notes[3]}', (0, 0, 0, 255), 'mm')

def song_info_draw(music: Music) -> Image.Image:
    img = Image.open(maimai_dir / 'song_bg.png').convert('RGBA')
    draw = ImageDraw.Draw(img)
    yh_font = DrawText(draw, YAHEI)

    cover = get_music_cover(music.id).resize((380, 380))
    tp = Image.open(maimai_dir / f'{music.type.upper()}.png')
    ver = Image.open(maimai_dir / f'{music.basic_info.version}.png')

    img.alpha_composite(cover, (235, 185))
    img.alpha_composite(tp, (1400, 280))
    img.alpha_composite(ver, (1250, 400))

    # Draw Title, Artist, and Basic Info
    yh_font.draw(740, 220, 60, music.title, (0, 0, 0, 255), 'lm')
    yh_font.draw(738, 300, 30, music.basic_info.artist, (0, 0, 0, 255), 'lm')
    yh_font.draw(738, 400, 38, f'ID {music.id}', (0, 0, 0, 255), 'lm')
    yh_font.draw(738, 460, 38, f'BPM {music.basic_info.bpm}', (0, 0, 0, 255), 'lm')
    yh_font.draw(738, 520, 38, f'分类 {music.basic_info.genre}', (0, 0, 0, 255), 'lm')

    # Draw Header for the stats
    yh_font.draw(480, 700, 40, f'拟合定数', (0, 0, 0, 255), 'mm')
    yh_font.draw(665, 700, 40, f'TOTAL', (0, 0, 0, 255), 'mm')
    yh_font.draw(835, 700, 40, f'TAP', (0, 0, 0, 255), 'mm')
    yh_font.draw(1015, 700, 40, f'HOLD', (0, 0, 0, 255), 'mm')
    yh_font.draw(1185, 700, 40, f'SLIDE', (0, 0, 0, 255), 'mm')
    yh_font.draw(1360, 700, 40, f'TOUCH', (0, 0, 0, 255), 'mm')
    yh_font.draw(1535, 700, 40, f'BREAK', (0, 0, 0, 255), 'mm')

    # Draw Level and Stats Info
    level_list = ['Basic', 'Advanced', 'Expert', 'Master']
    for i in range(4):  # For BASIC, ADVANCED, EXPERT, MASTER
        yh_font.draw(280, 835 + i * 135 - 30, 30, f'{level_list[i]}', (255, 255, 255, 255), 'mm')
        draw_level_info(yh_font, 835 + i * 135 - 30, music, i)
        draw_stats_info(yh_font, music, 135 * i, i)

    # Re:MASTER Level if exists
    yh_font.draw(280, 1350, 30, f'Re:Master', (255, 255, 255, 255), 'mm')
    if len(music.level) > 4:
        yh_font.draw(280, 1380, 30, f'{music.level[4]}({music.ds[4]})', (255, 255, 255, 255), 'mm')
        yh_font.draw(280, 1410, 20, f'{music.charts[4].charter}', (255, 255, 255, 255), 'mm')
        draw_stats_info(yh_font, music, 135 * 4, 4)

    return img

def send_song(targets: List[Music]) -> Message:
    if len(targets) == 1:
        target = targets[0]
        msg = Message()
        return msg.append(MessageSegment.image(image_to_base64(song_info_draw(target))))
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
