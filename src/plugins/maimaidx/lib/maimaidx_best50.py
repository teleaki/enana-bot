import math
from nonebot.adapters.onebot.v11 import MessageSegment

from .maimaidx_error import *
from .maimaidx_image import *
from .maimaidx_model import *
from .maimaidx_tool import *
from .maimaidx_user import get_plate_diy
from .maimaidx_music import mai


class DrawBest:
    basic = Image.open(maimai_dir / 'b50_score_basic.png')
    advanced = Image.open(maimai_dir / 'b50_score_advanced.png')
    expert = Image.open(maimai_dir / 'b50_score_expert.png')
    master = Image.open(maimai_dir / 'b50_score_master.png')
    remaster = Image.open(maimai_dir / 'b50_score_remaster.png')
    _diff = [basic, advanced, expert, master, remaster]

    def __init__(self, user_info: UserInfo, qqid: Optional[Union[int, str]] = None):
        self.nickname = user_info.nickname
        self.plate = user_info.plate
        self.addRating = user_info.additional_rating
        self.Rating = user_info.rating
        self.sdBest = user_info.charts.sd
        self.dxBest = user_info.charts.dx
        self.qqid = qqid

        self._im = Image.new('RGBA', (2200, 2500), color='white')

    def _findRaPic(self) -> str:
        if self.Rating < 1000:
            num = '01'
        elif self.Rating < 2000:
            num = '02'
        elif self.Rating < 4000:
            num = '03'
        elif self.Rating < 7000:
            num = '04'
        elif self.Rating < 10000:
            num = '05'
        elif self.Rating < 12000:
            num = '06'
        elif self.Rating < 13000:
            num = '07'
        elif self.Rating < 14000:
            num = '08'
        elif self.Rating < 14500:
            num = '09'
        elif self.Rating < 15000:
            num = '10'
        else:
            num = '11'
        return f'UI_CMN_DXRating_{num}.png'

    def _findMatchLevel(self) -> str:
        if self.addRating <= 10:
            num = f'{self.addRating:02d}'
        else:
            num = f'{self.addRating + 1:02d}'
        return f'UI_DNM_DaniPlate_{num}.png'

    def whiledraw(self, data: List[ChartInfo], font: DrawText, y: int) -> None:
        # y为第一排纵向坐标，dy为各排间距
        x = 70;  dy = 170
        TEXT_COLOR = [(255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255), (138, 0, 226, 255)]

        for num, info in enumerate(data):
            if num % 5 == 0:
                x = 70
                y += dy if num != 0 else 0
            else:
                x += 416

            cover = Image.open(get_music_cover(info.song_id)).resize((135, 135))
            version = Image.open(maimai_dir / f'{info.type.upper()}.png').resize((55, 19))
            if info.rate.islower():
                rate = Image.open(maimai_dir / f'UI_TTR_Rank_{score_Rank_l[info.rate]}.png').resize((95, 44))
            else:
                rate = Image.open(maimai_dir / f'UI_TTR_Rank_{info.rate}.png').resize((95, 44))

            self._im.alpha_composite(self._diff[info.level_index], (x, y))
            self._im.alpha_composite(cover, (x + 5, y + 5))
            self._im.alpha_composite(version, (x + 80, y + 141))
            self._im.alpha_composite(rate, (x + 150, y + 98))
            if info.fc:
                fc = Image.open(maimai_dir / f'UI_MSS_MBase_Icon_{fcl[info.fc]}.png').resize((45, 45))
                self._im.alpha_composite(fc, (x + 246, y + 99))
            if info.fs:
                fs = Image.open(maimai_dir / f'UI_MSS_MBase_Icon_{fsl[info.fs]}.png').resize((45, 45))
                self._im.alpha_composite(fs, (x + 291, y + 99))

            dxscore = sum(mai.total_list.search_by_id(str(info.song_id)).charts[info.level_index].notes) * 3
            dxnum = dxScore(info.dxScore / dxscore * 100)
            if dxnum:
                self._im.alpha_composite(Image.open(maimai_dir / f'UI_GAM_Gauge_DXScoreIcon_0{dxnum}.png'), (x + 335, y + 102))

            font.draw(x + 40, y + 148, 20, info.song_id, TEXT_COLOR[info.level_index], anchor='mm')
            title = info.title
            if coloumWidth(title) > 18:
                title = changeColumnWidth(title, 17) + '...'
            font.draw(x + 155, y + 20, 20, title, TEXT_COLOR[info.level_index], anchor='lm')
            font.draw(x + 155, y + 50, 32, f'{info.achievements:.4f}%', TEXT_COLOR[info.level_index], anchor='lm')
            font.draw(x + 338, y + 82, 15, f'{info.dxScore}/{dxscore}', TEXT_COLOR[info.level_index], anchor='mm')
            font.draw(x + 155, y + 82, 20, f'{info.ds} -> {info.ra}', TEXT_COLOR[info.level_index], anchor='lm')


    async def draw_b50(self) -> Image.Image:
        draw = ImageDraw.Draw(self._im)
        yh_font = DrawText(draw, YAHEI)

        dx_rating = Image.open(maimai_dir / self._findRaPic()).resize((300, 59))
        Name = Image.open(maimai_dir / 'Name.png')
        MatchLevel = Image.open(maimai_dir / self._findMatchLevel()).resize((134, 55))
        # ClassLevel = Image.open(maimai_dir / 'UI_FBR_Class_00.png').resize((144, 87))
        rating = Image.open(maimai_dir / 'UI_CMN_Shougou_Rainbow.png').resize((454, 50))
        icon = Image.open(maimai_dir / 'UI_Icon_309503.png').resize((214, 214))
        plate = None
        if self.qqid:
            icon = (await get_QQlogo(int(self.qqid))).resize((214, 214))
            plate_path = get_plate_diy(self.qqid)
            if plate_path:
                plate = Image.open(plate_path).resize((1420, 230))
        if not plate:
            if self.plate:
                plate = Image.open(plate_dir / f'{self.plate}.png').resize((1420, 230))
            else:
                plate = Image.open(get_random_file(other_plate_dir)).resize((1420, 230))

        self._im.alpha_composite(plate, (390, 100))
        self._im.alpha_composite(icon, (398, 108))
        self._im.alpha_composite(dx_rating, (620, 122))
        Rating = f'{self.Rating:05d}'
        for n, i in enumerate(Rating):
            self._im.alpha_composite(Image.open(maimai_dir / f'UI_NUM_Drating_{i}.png').resize((28, 34)), (760 + 23 * n, 137))
        self._im.alpha_composite(Name, (620, 200))
        self._im.alpha_composite(MatchLevel, (935, 205))
        # self._im.alpha_composite(ClassLevel, (926, 105))
        self._im.alpha_composite(rating, (620, 275))

        yh_font.draw(635, 235, 40, self.nickname, (0, 0, 0, 255), 'lm')
        sdrating, dxrating = sum([_.ra for _ in self.sdBest]), sum([_.ra for _ in self.dxBest])
        yh_font.draw(847, 295, 28, f'B35: {sdrating} + B15: {dxrating} = {self.Rating}', (0, 0, 0, 255), 'mm', 3,
                      (255, 255, 255, 255))

        self.whiledraw(self.sdBest, yh_font, 430)
        self.whiledraw(self.dxBest, yh_font, 1750)

        return self._im.resize((1760, 2000))

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

async def generate_b50(qqid: Optional[int] = None, username: Optional[str] = None) -> MessageSegment:
    try:
        if username:
            qqid = None
        obj = await maiapi.query_user('player', qqid=qqid, username=username)

        user_info = UserInfo(**obj)
        draw_best = DrawBest(user_info = user_info, qqid = qqid)

        pic = await draw_best.draw_b50()
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
    except TypeError as e:
        msg = MessageSegment.text(f"Error occurred: {e}")
    except Exception as e:
        msg = MessageSegment.text(f'未知错误：{type(e)}\n请联系Bot管理员')
    return msg

