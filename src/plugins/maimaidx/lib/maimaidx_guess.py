import asyncio
import random
from PIL import Image
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event
from nonebot.matcher import Matcher

from .maimaidx_res import *
from .maimaidx_model import *
from .maimaidx_image import *
from .maimaidx_music import mai, get_music_cover


class GuessMusic:
    def __init__(self):
        self.answer: Optional[Music] = None
        self.cover: Optional[Image.Image] = None
        self.timer_task = None

    def guess_music_start(self) -> Tuple[bool, Union[Message, MessageSegment]]:
        try:
            # 随机获取歌曲
            self.answer = random_music()
            if not self.answer:
                print('随机获取歌曲失败')
                return False, MessageSegment.text('随机获取歌曲失败，请重试')

            # 获取封面
            cover_path = get_music_cover(self.answer.id)
            if not cover_path:
                print(f'无法获取歌曲封面，歌曲ID: {self.answer.id}')
                return False, MessageSegment.text('无法获取封面，请重试')

            self.cover = Image.open(cover_path)
            if not self.cover:
                print(f'封面加载失败，歌曲ID: {self.answer.id}')
                return False, MessageSegment.text('封面加载失败，请重试')

            # 生成曲绘切片
            sample = get_sample(self.cover)
            if not sample:
                print(f'曲绘切片生成失败，歌曲ID: {self.answer.id}')
                return False, MessageSegment.text('曲绘切片生成失败，请重试')

            # 构建消息
            msg = Message([
                MessageSegment.text(
                    '开启mai看曲绘猜歌，你有180s的时间通过下面的曲绘切片猜出这是什么歌，发送“猜(id/title/alias)”进行游玩，发送“不玩了”结束游戏\n'),
                MessageSegment.image(image_to_base64(sample))
            ])
            return True, msg

        except Exception as e:
            print(f'猜歌游戏启动失败: {str(e)}')
            return False, MessageSegment.text('猜歌游戏启动失败，请重试')

    def guess_card_judge(self, key: Optional[str], qqid: Union[int, str]) -> Tuple[bool, Union[Message, MessageSegment]]:
        if key:
            alias_answer_ids = mai.total_alias_list.fuzzy_alias(key)
            alias_answer_id = alias_answer_ids[0]
            if key == self.answer.id or key == self.answer.title:
                msg = Message([
                    MessageSegment.text('恭喜'),
                    MessageSegment.at(qqid),
                    MessageSegment.text(f'答对了！是 {self.answer.id}: {self.answer.title} 哦\n'),
                    MessageSegment.image(image_to_base64(self.cover))
                ])
                return True, msg
            elif alias_answer_id == self.answer.id:
                msg = Message([
                    MessageSegment.text('恭喜'),
                    MessageSegment.at(qqid),
                    MessageSegment.text(f'答对了！是 {self.answer.id}: {self.answer.title} 哦\n'),
                    MessageSegment.image(image_to_base64(self.cover))
                ])
                return True, msg
            else:
                wrong_answer = mai.total_list.search_by_id(alias_answer_id)
                msg = Message([
                    MessageSegment.text(f'回答错误，不是 {wrong_answer.id}: {wrong_answer.title} 哦')
                ])
                return False, msg
        else:
            msg = Message([
                MessageSegment.text('请输入文字')
            ])
            return False, msg

    async def start_timer(self, matcher: Matcher, groupid: str, timeout: int = 180):
        """启动一个定时器，超时后自动结束游戏"""
        try:
            await asyncio.sleep(timeout - 60)

            # 构造消息
            msg = Message([
                MessageSegment.text('还剩60s，再给你点提示吧'),
                MessageSegment.text(f'这首歌的曲师是 {self.answer.basic_info.artist}')
            ])

            await matcher.send(msg)

            await asyncio.sleep(60)

            # 超时后结束游戏
            if groupid in games:
                msg = self.guess_music_timeout()
                self.guess_music_end()
                end_game(groupid)
                await matcher.finish(msg)
        except asyncio.CancelledError:
            # 任务被取消时的处理
            print(f"计时器已取消")

    def guess_music_timeout(self) -> Message:
        msg = Message([
            MessageSegment.text(f'很遗憾，没人能猜对，其实是 {self.answer.id}: {self.answer.title} 哦\n'),
            MessageSegment.image(image_to_base64(self.cover))
        ])
        return msg

    def guess_music_end(self):
        """结束游戏并取消计时器"""
        if self.timer_task:
            self.timer_task.cancel()  # 取消计时器任务
            self.timer_task = None  # 重置计时器任务引用

        self.answer = None
        self.cover = None

games: Dict[str, GuessMusic] = {}


def add_game(groupid: str) -> GuessMusic:
    # 创建一个新的 GuessMusic 实例并添加到 games 字典
    games[groupid] = GuessMusic()
    return games[groupid]


def end_game(groupid: str):
    """结束并清理指定群组的游戏实例"""
    if groupid in games:
        del games[groupid]

def get_sample(img: Image.Image, sample_width: int = 50, sample_height: int = 50) -> Image.Image:
    # 获取图片的宽度和高度
    width, height = img.size

    # 生成随机位置 (确保不超出图片边界)
    x = random.randint(0, width - sample_width)
    y = random.randint(0, height - sample_height)

    # 定义裁剪区域 (left, upper, right, lower)
    crop_area = (x, y, x + sample_width, y + sample_height)

    # 裁剪图片
    sample = img.crop(crop_area)

    return sample

def random_music(max_retries: int = 10) -> Optional[Music]:
    attempt = 0
    while attempt < max_retries:
        answer_id = random.randint(1, 12000)
        music = mai.total_list.search_by_id(answer_id)
        if music:
            return music
        else:
            attempt += 1
    return None

def get_group_id(event: Event) -> str:
    sessionid = event.get_session_id()
    groupid = sessionid.split('_')[1]
    return groupid

def is_started(groupid: str) -> bool:
    if groupid in games:
        return True
    return False