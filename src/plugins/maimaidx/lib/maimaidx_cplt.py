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
        self._im = Image.new('RGBA', (6140, 11200), color='white')

    def whiledraw(self, data: List[CpltInfo], font: DrawText, y: int, page: int) -> None:
        dy = 420
        TEXT_COLOR = [(255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255),
                      (138, 0, 226, 255)]

        for num, info in enumerate(data):
            if not num % 3:
                x = 50; y += dy
            else:
                x = 50 + (num % 3) * 2000 + (num % 3) * 20

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
            font.draw(x + 1580, y + 160, 50, f'No.{num + 1 + (page - 1) * 75}', TEXT_COLOR[info.level_index], anchor='rm')
            font.draw(x + 460, y + 150, 80, title, TEXT_COLOR[info.level_index], anchor='lm')
            font.draw(x + 450, y + 300, 120, f'{info.achievements:.4f}%', TEXT_COLOR[info.level_index], anchor='lm')

    async def draw_cplt(self, data: List[CpltInfo], arg: str, page: int, qqid: Optional[int]) -> Image.Image:
        draw = ImageDraw.Draw(self._im)
        yh_font = DrawText(draw, YAHEI)

        head = Image.open(maimai_dir / 'title2.png').resize((3000,600))
        self._im.alpha_composite(head, (1570, 50))

        icon = Image.open(maimai_dir / 'UI_Icon_309503.png').resize((50,50))
        if qqid:
            icon = (await get_QQlogo(qqid)).resize((400,400))
        self._im.alpha_composite(icon, (1800, 200))

        yh_font.draw(2800, 350, 120, arg, (0, 0, 0, 255), anchor='lm')

        self.whiledraw(data, yh_font, 200, page)

        return self._im.resize((3070,5600))


def get_page(data, page: int, size: int = 75):
    start_index = (page - 1) * size
    end_index = page * size
    return data[start_index:end_index]

def remove_duplicates(data: List[CpltInfo]) -> List[CpltInfo]:
    # 使用字典以 (id, level_index) 为键去重
    seen = {}  # 用来存储去重后的元素
    for info in data:
        key = (info.id, info.level_index)  # 根据 id 和 level_index 去重
        if key not in seen:
            seen[key] = info  # 如果 (id, level_index) 组合没有出现过，添加到字典中
    # 返回字典中的所有值，即去重后的元素列表
    return list(seen.values())

async def generate_level_cplt(level: str, page: int = 1, qqid: Optional[int] = None, username: Optional[str] = None) -> MessageSegment:
    try:
        if username:
            qqid = None
        version_list = list(plate_to_version.values())
        obj = await maiapi.query_user('plate', qqid=qqid, username=username, version=version_list)

        verlist = [CpltInfo(**item) for item in obj['verlist']]
        data = []
        for info in verlist:
            if info.level == level:
                data.append(info)

        data = remove_duplicates(data)
        data.sort(key=lambda x: x.achievements, reverse=True)
        max_page = len(data) // 75 + 1
        if page > max_page:
            page = max_page
        targets = get_page(data, page, size=75)

        arg = f'{level}分数列表 ({page}/{max_page})'

        draw_cplt = DrawCplt()
        pic = await draw_cplt.draw_cplt(targets, arg, page, qqid)

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