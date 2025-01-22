import json, aiofiles
from pathlib import Path
from typing import Any, Union

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


async def openfile(file: Path) -> Union[dict, list]:
    async with aiofiles.open(file, 'r', encoding='utf-8') as f:
        data = json.loads(await f.read())
    return data


async def writefile(file: Path, data: Any) -> bool:
    async with aiofiles.open(file, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=4))
    return True


class MaiMusic:

    total_list: MusicList
    # total_alias_list: AliasList

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
        # self.total_alias_list = await get_music_alias_list()

mai = MaiMusic()