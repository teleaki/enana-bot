from nonebot.adapters.onebot.v11 import MessageSegment, Message
import numpy as np

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

    def whiledraw(self, data: List[PlayInfo], font: DrawText, page: int, arg: str = None) -> None:
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

            font.draw(x + 12, y + 60, 60, f'#{(page - 1) * 70 + num + 1}', TEXT_COLOR[info.level_index], anchor='lm')
            font.draw(x + 410, y + 22, 25, title, TEXT_COLOR[info.level_index], anchor='lm')
            font.draw(x + 975, y + 32, 40, f'{info.achievements:.4f}%', TEXT_COLOR[info.level_index], anchor='rm')

            music = mai.total_list.search_by_id(info.id)

            ds = music.ds[info.level_index]
            font.draw(x + 410, y + 95, 25, f'定数：{ds}', TEXT_COLOR[info.level_index], anchor='lm')

            charter = music.charts[info.level_index].charter
            font.draw(x + 410, y + 60, 18, f'charter:{charter}', TEXT_COLOR[info.level_index], anchor='lm')

            bpm = music.basic_info.bpm
            font.draw(x + 575, y + 95, 25, f'BPM:{bpm}', TEXT_COLOR[info.level_index], anchor='lm')

    async def draw_table(self, data: List[PlayInfo], page: int = 1, qqid: Optional[int] = None, arg: str = None) -> Image.Image:
        draw = ImageDraw.Draw(self._im)
        yh_font = DrawText(draw, YAHEI)
        sf_font = DrawText(draw, SATISFY)

        max_page = len(data) // 70 + 1
        if page > max_page:
            page = max_page
        targets = get_page(data, page, size=70)

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

        info_list = vectorized_processing(data)
        for no, info in enumerate(info_list):
            yh_font.draw(40, (350 + no * 80), 40, info, (0, 0, 0, 255), anchor='lm')

        sf_font.draw(1000, 1270, 40, 'Generated by enana-bot', (0, 0, 0, 255), anchor='rm')

        self.whiledraw(targets, yh_font, page, arg=arg)

        return self._im.resize((1040,2640))


def get_page(data, page: int, size: int = 90):
    start_index = (page - 1) * size
    end_index = page * size
    return data[start_index:end_index]

def remove_duplicates_plate(data: List[PlayInfo]) -> List[PlayInfo]:
    # 使用字典以 (id, level_index) 为键去重
    seen = {}  # 用来存储去重后的元素
    for info in data:
        key = (info.id, info.level_index)  # 根据 id 和 level_index 去重
        if key not in seen:
            seen[key] = info  # 如果 (id, level_index) 组合没有出现过，添加到字典中
    # 返回字典中的所有值，即去重后的元素列表
    return list(seen.values())


def vectorized_processing(data):
    # 将数据转换为NumPy数组
    achievements = np.array([x.achievements for x in data])
    fc_types = np.array([x.fc for x in data])

    # 使用向量化操作计算所有指标
    counters = {
        # FC类型统计
        'app': np.sum(fc_types == 'app'),
        'ap': np.sum(fc_types == 'ap'),

        # 主成就区间
        'sssp': np.sum(achievements >= 100.5),
        'sss': np.sum((achievements >= 100.0) & (achievements < 100.5)),
        'ssp': np.sum((achievements >= 99.0) & (achievements < 100.0)),
        'ss': np.sum((achievements >= 98.0) & (achievements < 99.0)),
        's': np.sum((achievements >= 97.0) & (achievements < 98.0)),
        'cl': np.sum(achievements < 97.0),

        # 特殊子区间
        'ssspc': np.sum((achievements >= 100.4) & (achievements < 100.5)),
        'sssc': np.sum((achievements >= 99.9) & (achievements < 100.0))
    }

    # 计算聚合值
    total_num = len(data)
    ap_total = counters['ap'] + counters['app']
    sss_total = counters['sssp'] + counters['sss']

    # 构建分段统计
    breakdown = [
        counters['sssp'] + counters['sss'] + counters['ssp'],  # 99%+
        counters['sssp'] + counters['sss'] + counters['ssp'] + counters['ss'],  # 98%+
        counters['sssp'] + counters['sss'] + counters['ssp'] + counters['ss'] + counters['s']  # 97%+
    ]

    # 生成结果列表
    info_list = [
        f'总共有 {total_num} 个成绩，其中：',
        f' ',
        f'AP的成绩共 {ap_total} 个（AP+：{counters["app"]}）',
        f'SSS+以上：{counters["sssp"]}   |   SSS以上：{sss_total}',
        f'99%以上：{breakdown[0]}   |   98%以上：{breakdown[1]}',
        f'97%以上：{breakdown[2]}',
        f'未满97%：{counters["cl"]}',
        f' ',
        f'SSS+寸：{counters["ssspc"]}   |   SSS寸：{counters["sssc"]}'
    ]

    return info_list

def process_image(cover: Image.Image) -> Image.Image:
    # 转换为RGBA模式
    img = cover.convert("RGBA")

    # 高质量缩放至600x600
    img = img.resize((600, 600), Image.Resampling.LANCZOS)

    # 垂直居中裁剪600x240区域
    y_center = 300
    crop_area = (0, y_center - 120, 600, y_center + 120)
    cropped = img.crop(crop_area)

    # 使用NumPy创建渐变遮罩
    protect = 150
    width, height = 600, 240
    center_x = width // 2
    side_l = center_x - protect // 2  # 225
    side_r = center_x + protect // 2  # 375
    max_distance = (width - protect) / 2  # 225.0

    # 创建一维alpha数组
    alpha = np.zeros(width, dtype=np.uint8)

    # 左侧渐变区域 (0到224)
    x_left = np.arange(side_l)
    alpha[x_left] = (255 * (1 - (side_l - x_left) / max_distance)).astype(np.uint8)

    # 中央不透明区域 (225到374)
    alpha[side_l:side_r] = 255

    # 右侧渐变区域 (375到599)
    x_right = np.arange(side_r, width)
    alpha[x_right] = (255 * (1 - (x_right - side_r) / max_distance)).astype(np.uint8)

    # 扩展为二维遮罩并转换为图像
    gradient = Image.fromarray(np.tile(alpha, (height, 1)), mode='L')

    # 应用透明度
    cropped.putalpha(gradient)

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

        verlist = [PlayInfo(**item) for item in obj['verlist']]
        data = []
        for info in verlist:
            if info.level == level:
                data.append(info)

        data = remove_duplicates_plate(data)
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

        verlist = [PlayInfo(**item) for item in obj['verlist']]
        data = []
        for info in verlist:
            music = mai.total_list.search_by_id(info.id)
            for rc in real_charter_list:
                if music.charts[info.level_index].charter in real_charters[rc]:
                    data.append(info)

        data = remove_duplicates_plate(data)
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

        verlist = [PlayInfo(**item) for item in obj['verlist']]
        data = []
        for info in verlist:
            music = mai.total_list.search_by_id(info.id)
            if bpm_min <= music.basic_info.bpm <= bpm_max:
                data.append(info)

        data = remove_duplicates_plate(data)
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