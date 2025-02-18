from nonebot.adapters.onebot.v11 import MessageSegment, Message

from .maimaidx_error import *
from .maimaidx_image import *
from .maimaidx_model import *
from .maimaidx_tool import *
from .maimaidx_music import mai
from .maimaidx_res import *


class DrawTable:

    basic = Image.open(maimai_dir / 'cplt_basic.png')
    advanced = Image.open(maimai_dir / 'cplt_advanced.png')
    expert = Image.open(maimai_dir / 'cplt_expert.png')
    master = Image.open(maimai_dir / 'cplt_master.png')
    remaster = Image.open(maimai_dir / 'cplt_remaster.png')
    _diff = [basic, advanced, expert, master, remaster]

    def __init__(self):
        self._im = Image.new('RGBA', (2080, 5280), color=(4,33,67,255))

    def whiledraw(self, data: List[CpltInfo], font: DrawText, page: int, arg: str = None) -> None:
        dy = 130
        TEXT_COLOR = [(255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255),
                      (255, 255, 255, 255)]

        for num, info in enumerate(data):
            if num < 30:
                x = 30; y = 30 + dy * (num + 10)
            else:
                x = 1060; y = 30 + dy * (num - 30)

            cover = Image.open(get_music_cover(info.id))
            cover = process_image(cover).resize((300,120))
            ver = Image.open(maimai_dir / f'{info.type.upper()}.png').resize((105,36))

            # if info.rate.islower():
            #     rate = Image.open(maimai_dir / f'UI_TTR_Rank_{score_Rank_l[info.rate]}.png').resize((368,174))
            # else:
            #     rate = Image.open(maimai_dir / f'UI_TTR_Rank_{info.rate}.png').resize((368,174))

            self._im.alpha_composite((self._diff[info.level_index]).resize((1000,120)), (x, y))
            self._im.alpha_composite(cover, (x + 100, y + 0))
            self._im.alpha_composite(ver, (x + 750, y + 75))
            # self._im.alpha_composite(rate, (x + 1850, y + 240))

            if info.fc:
                fc = Image.open(maimai_dir / f'UI_MSS_MBase_Icon_{fcl[info.fc]}.png').resize((60,60))
                self._im.alpha_composite(fc, (x + 860, y + 62))
            if info.fs:
                fs = Image.open(maimai_dir / f'UI_MSS_MBase_Icon_{fsl[info.fs]}.png').resize((60,60))
                self._im.alpha_composite(fs, (x + 925, y + 62))

            title = f'{info.id}: {info.title}'
            if coloumWidth(title) > 17:
                title = changeColumnWidth(title, 16) + '...'

            font.draw(x + 12, y + 60, 60, f'#{(page - 1) * 120 + num + 1}', TEXT_COLOR[info.level_index], anchor='lm')
            font.draw(x + 410, y + 22, 25, title, TEXT_COLOR[info.level_index], anchor='lm')
            font.draw(x + 975, y + 32, 40, f'{info.achievements:.4f}%', TEXT_COLOR[info.level_index], anchor='rm')

            music = mai.total_list.search_by_id(info.id)

            ds = music.ds[info.level_index]
            font.draw(x + 410, y + 95, 25, f'定数：{ds}', TEXT_COLOR[info.level_index], anchor='lm')

            charter = music.charts[info.level_index].charter
            font.draw(x + 410, y + 60, 18, f'charter:{charter}', TEXT_COLOR[info.level_index], anchor='lm')

            bpm = music.basic_info.bpm
            font.draw(x + 575, y + 95, 25, f'BPM:{bpm}', TEXT_COLOR[info.level_index], anchor='lm')

    async def draw_table(self, data: List[CpltInfo], page: int = 1, qqid: Optional[int] = None, arg: str = None) -> Image.Image:
        draw = ImageDraw.Draw(self._im)
        yh_font = DrawText(draw, YAHEI)

        max_page = len(data) // 75 + 1
        if page > max_page:
            page = max_page
        targets = get_page(data, page, size=75)

        head = f'{arg}分数列表 ({page}/{max_page})'

        bg1 = create_rounded_rectangle((1020, 3910), 30)
        bg2 = create_rounded_rectangle((1020, 5210), 30)
        bg_info = create_rounded_rectangle((1020, 1030), 30)
        bg_head = create_rounded_rectangle((520, 100), 30)

        self._im.alpha_composite(bg1, (20, 1320))
        self._im.alpha_composite(bg2, (1050, 20))
        self._im.alpha_composite(bg_info, (20, 280))
        self._im.alpha_composite(bg_head, (320, 100))

        icon = Image.open(maimai_dir / 'UI_Icon_309503.png').resize((140,140))
        if qqid:
            icon = (await get_QQlogo(qqid)).resize((140,140))
        self._im.alpha_composite(icon, (150, 50))

        yh_font.draw(580, 150, 40, head, (0, 0, 0, 255), anchor='mm')

        yh_font.draw(580, 150, 40, head, (0, 0, 0, 255), anchor='mm')

        self.whiledraw(targets, yh_font, page, arg=arg)

        return self._im


def get_page(data, page: int, size: int = 90):
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

def process_image(cover: Image.Image) -> Image.Image:
    # 打开图片并确保RGBA模式
    img = cover.convert("RGBA")

    # 放大到600x600（使用高质量缩放）
    img = img.resize((600, 600), Image.Resampling.LANCZOS)

    # 计算裁剪区域（垂直居中600x240）
    y_center = 300  # 原图高度600的中间点
    crop_area = (0, y_center - 120, 600, y_center + 120)  # 600x240区域
    cropped = img.crop(crop_area)

    # 创建水平渐变透明度遮罩
    protect = 150
    width, height = 600, 240
    gradient = Image.new("L", (width, height))
    center_x = width // 2
    side_l = center_x - protect // 2
    side_r = center_x + protect // 2
    max_distance = (width - protect) / 2

    # 逐像素设置透明度
    for x in range(side_l):
        # 计算当前x坐标到中心的距离比例（0.0~1.0）
        distance = abs(x - side_l) / max_distance
        # 透明度从两边0%到中心100%（alpha值255~0）
        alpha = int(255 * (1 - distance))
        # 为整列设置相同透明度
        for y in range(height):
            gradient.putpixel((x, y), alpha)

    for x in range(side_l, side_r):
        for y in range(height):
            gradient.putpixel((x, y), 255)

    for x in range(side_r, width):
        # 计算当前x坐标到中心的距离比例（0.0~1.0）
        distance = abs(x - side_r) / max_distance
        # 透明度从两边0%到中心100%（alpha值255~0）
        alpha = int(255 * (1 - distance))
        # 为整列设置相同透明度
        for y in range(height):
            gradient.putpixel((x, y), alpha)

    # 应用透明度到裁剪后的图片
    cropped.putalpha(gradient)

    # 保存结果
    return cropped

def create_rounded_rectangle(
        size: tuple[int, int],
        radius: int,
        border_width: int = 3
) -> Image.Image:
    """
    生成带黑边框的白底圆角矩形

    参数：
    size: (宽度, 高度) 单位像素
    radius: 圆角半径 (建议值：10-40)
    border_width: 边框宽度 (默认3像素)

    返回：
    PIL.Image对象 (RGB模式)
    """
    # 创建白色画布
    width, height = size
    image = Image.new("RGBA", size, color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # 绘制黑边框圆角矩形
    draw.rounded_rectangle(
        [(0, 0), (width - 1, height - 1)],  # 覆盖整个画布
        radius=radius,
        fill="white",  # 内部填充色
        outline="black",  # 边框颜色
        width=border_width  # 边框粗细
    )

    return image

async def generate_level_table(level: str, page: int = 1, qqid: Optional[int] = None, username: Optional[str] = None) -> MessageSegment:
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

        draw_cplt = DrawTable()
        pic = await draw_cplt.draw_table(data, page, qqid, arg=level)

        msg = MessageSegment.image(image_to_base64(pic))
    except UserNotFoundError as e:
        msg = MessageSegment.text(str(e))
    except UserDisabledQueryError as e:
        msg = MessageSegment.text(str(e))
    except Exception as e:
        msg = MessageSegment.text(f'{type(e)}: {e}\n请联系Bot管理员')
    return msg

async def generate_charter_table(charter: str, page: int = 1, qqid: Optional[int] = None, username: Optional[str] = None) -> Message:
    try:
        if username:
            qqid = None
        version_list = list(plate_to_version.values())
        obj = await maiapi.query_user('plate', qqid=qqid, username=username, version=version_list)

        real_charter_list = []
        for rc in real_charters.keys():
            if charter.lower() in rc.lower():
                real_charter_list.append(rc)

        real_charter_list = list(dict.fromkeys(real_charter_list))

        verlist = [CpltInfo(**item) for item in obj['verlist']]
        data = []
        for info in verlist:
            music = mai.total_list.search_by_id(info.id)
            for rc in real_charter_list:
                if music.charts[info.level_index].charter in real_charters[rc]:
                    data.append(info)

        data = remove_duplicates(data)
        data.sort(key=lambda x: x.achievements, reverse=True)

        charter_info = Message([
            MessageSegment.text('匹配到的谱师有：\n')
        ])
        for rc in real_charter_list:
            charter_info.append(MessageSegment.text(', '.join(real_charters[rc])))

        draw_cplt = DrawTable()
        pic = await draw_cplt.draw_table(data, page, qqid, arg=charter)

        msg = charter_info + MessageSegment.image(image_to_base64(pic))
    except UserNotFoundError as e:
        msg = MessageSegment.text(str(e))
    except UserDisabledQueryError as e:
        msg = MessageSegment.text(str(e))
    except Exception as e:
        msg = MessageSegment.text(f'{type(e)}: {e}\n请联系Bot管理员')
    return msg

async def generate_bpm_table(bpm_min: int, bpm_max: int, page: int = 1, qqid: Optional[int] = None, username: Optional[str] = None) -> Message:
    try:
        if username:
            qqid = None
        version_list = list(plate_to_version.values())
        obj = await maiapi.query_user('plate', qqid=qqid, username=username, version=version_list)

        verlist = [CpltInfo(**item) for item in obj['verlist']]
        data = []
        for info in verlist:
            music = mai.total_list.search_by_id(info.id)
            if bpm_min <= music.basic_info.bpm <= bpm_max:
                data.append(info)

        data = remove_duplicates(data)
        data.sort(key=lambda x: x.achievements, reverse=True)

        draw_cplt = DrawTable()
        pic = await draw_cplt.draw_table(data, page, qqid, arg=f'{bpm_min}-{bpm_max}')

        bpm_info = Message([
            MessageSegment.text('查询的BPM范围为：\n'),
            MessageSegment.text(f'[{bpm_min}, {bpm_max}]')
        ])

        msg = bpm_info + MessageSegment.image(image_to_base64(pic))
    except UserNotFoundError as e:
        msg = MessageSegment.text(str(e))
    except UserDisabledQueryError as e:
        msg = MessageSegment.text(str(e))
    except Exception as e:
        msg = MessageSegment.text(f'{type(e)}: {e}\n请联系Bot管理员')
    return msg