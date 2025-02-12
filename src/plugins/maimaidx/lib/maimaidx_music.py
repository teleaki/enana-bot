from rapidfuzz import process, fuzz

from .maimaidx_api import maiapi
from .maimaidx_model import *
from .maimaidx_tool import *
from .maimaidx_res import *


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

class AliasList:
    def __init__(self, alias_data: Dict[str, List[str]]):
        """
        直接从 {id: [别名]} 结构初始化，无需 Alias 对象
        """
        self.alias_dict: Dict[str, List[str]] = alias_data  # 直接存储 {id: [别名]}
        self.alias_map: Dict[str, str] = {}  # {别名: id}
        self.alias_strings: List[str] = []  # 存储所有别名列表

        # 直接构建映射，避免中间对象
        for music_id, aliases in alias_data.items():
            for alias in aliases:
                if alias not in self.alias_map:  # 避免重复存储
                    self.alias_map[alias] = music_id
                    self.alias_strings.append(alias)

    def get_alias_by_id(self, music_id: str) -> Optional[List[str]]:
        """通过 ID 获取别名列表"""
        return self.alias_dict.get(music_id)

    def fuzzy_alias(self, input_str: str) -> Optional[List[str]]:
        """使用 rapidfuzz 进行模糊匹配，返回所有相似度大于 90 的匹配项，
        如果没有，则返回相似度大于 70 且最接近的匹配项"""
        if not isinstance(input_str, str) or not self.alias_strings:
            return None

        # 获取所有匹配的结果
        matches = process.extract(input_str, self.alias_strings, scorer=fuzz.ratio)

        # 筛选出相似度大于 90 的匹配项
        result_ids = []
        max_score = 0
        best_match_id = None

        for best_match, score, _ in matches:
            if score > 90:
                result_ids.append(self.alias_map[best_match])  # 获取符合条件的 ID
            elif score > max_score and score > 70:
                max_score = score
                best_match_id = self.alias_map[best_match]  # 获取最接近的 ID

        # 如果找到了相似度大于 90 的匹配项
        if result_ids:
            return result_ids

        # 如果没有，返回相似度大于 70 且最高的 ID
        if best_match_id:
            return [best_match_id]

        return None  # 没有匹配项


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

        # # 将字典重构为Alias
        # alias_rebuild: List[Alias] = []
        # for key, values in alias_data.items():
        #     alias_rebuild.append(Alias(id=key, aliases=values))

        self.total_alias_list = AliasList(alias_data=alias_data)

mai = MaiMusic()