from nonebot.adapters.onebot.v11 import MessageSegment

from .maimaidx_api import maiapi
from .maimaidx_error import *
from .maimaidx_image import *
from .maimaidx_model import *
from .maimaidx_music import get_music_cover
from .maimaidx_res import *


class DrawCplt:

    basic = Image.open(maimai_dir / 'cplt_basic.png')
    advanced = Image.open(maimai_dir / 'cplt_advanced.png')
    expert = Image.open(maimai_dir / 'cplt_expert.png')
    master = Image.open(maimai_dir / 'cplt_master.png')
    remaster = Image.open(maimai_dir / 'cplt_remaster.png')
    _diff = [basic, advanced, expert, master, remaster]

    def __init__(self):
        self._im = Image.new('RGBA', (6120, 9000), color='white')

    def whiledraw(self, data: List[CpltInfo], font: DrawText, y:int) -> None:
        dy = 410
        TEXT_COLOR = [(255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255),
                      (138, 0, 226, 255)]

        for num, info in enumerate(data):
            if not num % 3:
                x = 50; y += dy
            else:
                x = 50 + (num % 3) * 2000 + (num % 3 - 1) * 10

            cover = get_music_cover(info.id).resize((280,280))
            ver = Image.open(maimai_dir / f'{info.type.upper()}.png').resize((210,78))

            # if info.rate.islower():
            #     rate = Image.open(maimai_dir / f'UI_TTR_Rank_{score_Rank_l[info.rate]}.png').resize((368,174))
            # else:
            #     rate = Image.open(maimai_dir / f'UI_TTR_Rank_{info.rate}.png').resize((368,174))

            self._im.alpha_composite(self._diff[info.level_index], (x, y))
            self._im.alpha_composite(cover, (x + 60, y + 60))
            self._im.alpha_composite(ver, (x + 1600, y + 125))
            # self._im.alpha_composite(rate, (x + 1850, y + 240))

            if info.fc:
                fc = Image.open(maimai_dir / f'UI_MSS_MBase_Icon_{fcl[info.fc]}.png').resize((200,200))
                self._im.alpha_composite(fc, (x + 1450, y + 220))
            if info.fs:
                fs = Image.open(maimai_dir / f'UI_MSS_MBase_Icon_{fsl[info.fs]}.png').resize((200,200))
                self._im.alpha_composite(fs, (x + 1650, y + 220))

            title = f'{info.id}: {info.title}'
            if coloumWidth(title) > 17:
                title = changeColumnWidth(title, 16) + '...'
            font.draw(x + 1580, y + 160, 50, f'No.{num + 1}', TEXT_COLOR[info.level_index], anchor='rm')
            font.draw(x + 460, y + 150, 80, title, TEXT_COLOR[info.level_index], anchor='lm')
            font.draw(x + 450, y + 300, 120, f'{info.achievements:.4f}%', TEXT_COLOR[info.level_index], anchor='lm')

    def draw_cplt(self, data: List[CpltInfo], arg: str) -> Image.Image:
        draw = ImageDraw.Draw(self._im)
        yh_font = DrawText(draw, YAHEI)

        head = Image.open(maimai_dir / 'title2.png').resize((2000,400))
        self._im.alpha_composite(head, (2060, 100))

        yh_font.draw(3060, 300, 100, arg, (0, 0, 0, 255), anchor='mm')

        self.whiledraw(data, yh_font, 200)

        return self._im.resize((3060,4500))


async def generate_level_cplt(level: str, qqid: Optional[int] = None, username: Optional[str] = None) -> MessageSegment:
    try:
        if username:
            qqid = None
        version_list = list(plate_to_version.values())
        obj = await maiapi.query_user('plate', qqid=qqid, username=username, version=version_list)

        verlist = [CpltInfo(**item) for item in obj['verlist']]
        targets = []
        for info in verlist:
            if info.level == level:
                targets.append(info)

        arg = f'{level}分数列表'

        draw_cplt = DrawCplt()
        pic = draw_cplt.draw_cplt(targets[:50], arg)

        msg = MessageSegment.image(image_to_base64(pic))
    except UserNotFoundError as e:
        msg = MessageSegment.text(str(e))
    except UserDisabledQueryError as e:
        msg = MessageSegment.text(str(e))
    except OSError as e:
        msg = MessageSegment.text(f"Error occurred: {e}")
    except AttributeError as e:
        msg = MessageSegment.text(f"Error occurred: {e}")
    except ValueError as e:
        msg = MessageSegment.text(f"Error occurred: {e}")
    except Exception as e:
        msg = MessageSegment.text(f'未知错误：{type(e)}\n请联系Bot管理员')
    return msg