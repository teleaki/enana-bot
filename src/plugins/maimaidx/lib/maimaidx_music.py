import json, aiofiles
from pathlib import Path
from typing import Any, Union

from PIL import Image

from .maimaidx_res import *
from .maimaidx_error import *
from .maimaidx_model import *
from .maimaidx_api import maiapi


class MusicList(List[Music]):
    def search_by_id(self, music_id: Union[str, int]) -> Optional[Music]:
        for music in self:
            if music.id == str(music_id):
                return music
        return None

    def search_by_title(self, music_title: str) -> Optional[Music]:
        for music in self:
            if music.title == music_title:
                return music
        return None

class AliasList(List[Alias]):
    def alias2id(self, music_alias: str) -> Optional[str]:
        for alias in self:
            if music_alias in alias.aliases:
                return alias.id
        return None

    def id2alias(self, music_id: Union[str, int] = None) -> Optional[List[str]]:
        if music_id:
            for alias in self:
                if alias.id == str(music_id):
                    return alias.aliases
            return None
        else:
            return None


async def openfile(file: Path) -> Union[dict, list]:
    async with aiofiles.open(file, 'r', encoding='utf-8') as f:
        data = json.loads(await f.read())
    return data


async def writefile(file: Path, data: Any) -> bool:
    async with aiofiles.open(file, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=4))
    return True


def get_music_cover(music_id: Union[str, int]) -> Image.Image:
    cover_path = cover_dir / f'{int(music_id)}.png'
    cover_path_sd = cover_dir / f'{int(music_id) - 10000}.png'
    cover_path_dx = cover_dir / f'{int(music_id) + 10000}.png'
    # 检查文件是否存在，若不存在则使用默认的 0.png
    if cover_path.exists():
        cover = Image.open(cover_path).resize((135, 135))
    elif cover_path_sd.exists():
        cover = Image.open(cover_path_sd).resize((135, 135))
    elif cover_path_dx.exists():
        cover = Image.open(cover_path_dx).resize((135, 135))
    else:
        cover = Image.open(cover_dir / '0.png').resize((135, 135))  # 使用默认的 0.png
    return cover


class MaiMusic:

    total_list: MusicList
    total_alias_list: AliasList

    def __init__(self) -> None:
        """封装所有曲目信息以及猜歌数据，便于更新"""

    async def get_music_list(self) -> None:
        """获取所有数据"""
        # MusicData
        try:
            try:
                music_data = await maiapi.music_data()
                await writefile(music_file, music_data)
            except Exception:
                # 从diving-fish获取maimaiDX曲目数据失败,切换至本地暂存文件
                music_data = await openfile(music_file)
        except FileNotFoundError:
            # 未找到文件，请自行使用浏览器访问 "https://www.diving-fish.com/api/maimaidxprober/music_data" 将内容保存为 "music_data.json" 存放在 "static" 目录下并重启bot
            raise

        # ChartStats
        try:
            try:
                chart_stats = await maiapi.chart_stats()
                await writefile(chart_file, chart_stats)
            except Exception:
                # 从diving-fish获取maimaiDX曲目数据失败,切换至本地暂存文件
                chart_stats = await openfile(chart_file)
        except FileNotFoundError:
            # 未找到文件，请自行使用浏览器访问 "https://www.diving-fish.com/api/maimaidxprober/chart_stats" 将内容保存为 "chart_stats.json" 存放在 "static" 目录下并重启bot
            raise

        self.total_list = MusicList()
        for music in music_data:
            if music['id'] in chart_stats['charts']:
                _stats = [_data if _data else None for _data in chart_stats['charts'][music['id']]] if {} in chart_stats[
                    'charts'][music['id']] else chart_stats['charts'][music['id']]
            else:
                _stats = None
            self.total_list.append(Music(stats=_stats, **music))

    async def get_music_alias(self) -> None:
        """获取所有曲目别名"""
        try:
            try:
                alias_data = await maiapi.music_alias()
                await writefile(alias_file, alias_data)
            except Exception:
                # 从diving-fish获取maimaiDX曲目数据失败,切换至本地暂存文件
                alias_data = await openfile(alias_file)
        except FileNotFoundError:
            # 未找到文件，请自行使用浏览器访问 "https://download.fanyu.site/maimai/alias.json" 将内容保存为 "alias_data.json" 存放在 "static" 目录下并重启bot
            raise

        # 将字典重构为Alias
        alias_rebuild: List[Alias] = []
        for key, values in alias_data.items():
            alias_rebuild.append(Alias(id=key, aliases=values))

        self.total_alias_list = AliasList(alias_rebuild)

mai = MaiMusic()