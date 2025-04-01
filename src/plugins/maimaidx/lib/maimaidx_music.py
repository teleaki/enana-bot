import os
import threading

from PIL import Image, ImageDraw, ImageFont
from typing import List
import io

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

    def fuzzy_alias(self, input_str: str, threshold: int = 70) -> Optional[List[str]]:
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
            elif score > max_score and score > threshold:
                max_score = score
                best_match_id = self.alias_map[best_match]  # 获取最接近的 ID

        # 如果找到了相似度大于 90 的匹配项
        if result_ids:
            return result_ids

        # 如果没有，返回相似度大于 70 且最高的 ID
        if best_match_id:
            return [best_match_id]

        return None  # 没有匹配项


async def add_local_alias(id: str, alias: str) -> int:
    """添加本地别名到指定ID

    Args:
        id: 目标ID
        alias: 要添加的别名

    Returns:
        AliasStatus状态码
    """

    class AliasStatus:
        SUCCESS = 0
        ALIAS_EXISTS = 1
        INVALID_DATA = 2
        WRITE_ERROR = 3

    file_lock = threading.Lock()

    if not isinstance(alias, str):
        return AliasStatus.INVALID_DATA

    with file_lock:
        try:
            # 原子化读取操作
            if local_alias_file.exists():
                with open(local_alias_file, 'r', encoding='utf-8') as f:
                    try:
                        data: Dict[str, List[str]] = json.load(f)
                    except json.JSONDecodeError:
                        data = {}
            else:
                data = {}

            # 初始化数据结构
            if not isinstance(data, dict):
                data = {}

            # 确保该ID对应的值是列表
            alias_list = data.setdefault(id, [])

            # 类型安全检查
            if not isinstance(alias_list, list):
                data[id] = [str(alias_list)]  # 转换现有值为列表
                alias_list = data[id]

            # 检查别名是否存在
            if alias in alias_list:
                return AliasStatus.ALIAS_EXISTS

            # 添加新别名
            alias_list.append(alias)

            # 原子化写入操作
            temp_file = local_alias_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            # 替换原文件
            temp_file.replace(local_alias_file)

            await mai.get_music_alias(arg=1)

            return AliasStatus.SUCCESS

        except (IOError, PermissionError) as e:
            print(f"文件操作失败: {str(e)}")
            return AliasStatus.WRITE_ERROR
        except Exception as e:
            print(f"未知错误: {str(e)}")
            return AliasStatus.INVALID_DATA


async def del_local_alias(id: str, alias: str) -> int:
    """删除指定ID的别名

    Args:
        id: 目标用户ID
        alias: 要删除的别名

    Returns:
        AliasStatus状态码
    """
    class AliasStatus:
        SUCCESS = 0
        ALIAS_NOT_FOUND = 1
        ID_NOT_EXIST = 2
        INVALID_DATA = 3
        WRITE_ERROR = 4

    file_lock = threading.Lock()

    if not isinstance(alias, str) or not alias:
        return AliasStatus.INVALID_DATA

    with file_lock:
        try:
            # 原子化读取操作
            if local_alias_file.exists():
                with open(local_alias_file, 'r', encoding='utf-8') as f:
                    try:
                        data: Dict[str, List[str]] = json.load(f)
                    except json.JSONDecodeError:
                        data = {}
            else:
                return AliasStatus.ID_NOT_EXIST

            # 数据结构校验
            if not isinstance(data, dict):
                data = {}

            # 检查ID是否存在
            if id not in data:
                return AliasStatus.ID_NOT_EXIST

            # 获取别名列表并进行类型检查
            alias_list = data[id]
            if not isinstance(alias_list, list):
                data[id] = [str(alias_list)]  # 尝试修复数据
                alias_list = data[id]

            # 执行删除操作
            try:
                alias_list.remove(alias)
            except ValueError:
                return AliasStatus.ALIAS_NOT_FOUND

            # 清理空列表
            if len(alias_list) == 0:
                del data[id]

            # 原子化写入操作
            temp_file = local_alias_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            # 替换原文件
            if data:  # 仅当有数据时保留文件
                temp_file.replace(local_alias_file)
            else:  # 无数据时删除文件
                os.remove(temp_file)
                if local_alias_file.exists():
                    os.remove(local_alias_file)

            await mai.get_music_alias(arg=1)

            return AliasStatus.SUCCESS

        except (IOError, PermissionError) as e:
            print(f"文件操作失败: {str(e)}")
            return AliasStatus.WRITE_ERROR
        except Exception as e:
            print(f"未知错误: {str(e)}")
            return AliasStatus.INVALID_DATA

async def show_all_alias(id: str) -> (bool, Optional[Image]):
    """显示指定ID在local_alias_file和alias_file中的所有别名

    Args:
        id: 目标ID

    Returns:
        包含所有别名的列表
    """

    all_aliases = set()  # 使用集合以确保别名不重复

    # 读取local_alias_file
    try:
        if local_alias_file.exists():
            with open(local_alias_file, 'r', encoding='utf-8') as f:
                try:
                    data: Dict[str, List[str]] = json.load(f)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}

        # 如果id存在，添加到all_aliases
        if id in data:
            all_aliases.update(data[id])
    except (IOError, PermissionError) as e:
        print(f"读取local_alias_file失败: {str(e)}")
        return Image.new('RGB', (800, 600), (255, 255, 255))  # 返回空白图片

    # 读取alias_file
    try:
        if alias_file.exists():
            with open(alias_file, 'r', encoding='utf-8') as f:
                try:
                    data: Dict[str, List[str]] = json.load(f)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}

        # 如果id存在，添加到all_aliases
        if id in data:
            all_aliases.update(data[id])
    except (IOError, PermissionError) as e:
        print(f"读取alias_file失败: {str(e)}")
        return False, None

    # 如果没有找到任何别名，返回空白图片
    if not all_aliases:
        return False, None

    # 调用generate_alias_image函数生成图片
    image = await generate_alias_image(list(all_aliases))

    return True, image


async def generate_alias_image(all_aliases: List[str]) -> Image:
    """将别名列表渲染为文字图片

    Args:
        all_aliases: 包含所有别名的列表

    Returns:
        返回生成的PIL Image对象
    """
    # 设置图片宽度和背景颜色
    width = 300
    background_color = (255, 255, 255)  # 白色背景
    text_color = (0, 0, 0)  # 黑色文字

    # 创建一个 ImageDraw 对象来绘制文本
    draw = ImageDraw.Draw(Image.new('RGB', (width, 1), background_color))  # 先创建一个临时图片来计算文本高度

    # 设置字体和字号
    try:
        font = ImageFont.truetype("YAHEI", 50)  # 如果没有arial.ttf，可以换成默认字体
    except IOError:
        font = ImageFont.load_default()  # 如果找不到ttf文件，使用默认字体

    # 设置行间距
    line_height = 25  # 默认行间距

    total_height = 10  # 初始y坐标，加上顶部间距

    # 计算所有别名的高度
    for alias in all_aliases:
        # 使用getbbox()来计算文本边界框
        bbox = draw.textbbox((0, 0), alias, font=font)
        text_height = bbox[3] - bbox[1]  # 获取文本高度

        total_height += text_height + line_height  # 累加每行文本的高度和行间距

    # 创建最终的图片，使用计算得到的动态高度
    img = Image.new('RGB', (width, total_height), background_color)
    draw = ImageDraw.Draw(img)

    y_position = 10  # 初始y坐标

    # 将所有别名写入图片
    for alias in all_aliases:
        # 使用getbbox()来计算文本边界框
        bbox = draw.textbbox((0, 0), alias, font=font)
        text_height = bbox[3] - bbox[1]  # 获取文本高度

        # 绘制文本
        draw.text((10, y_position), alias, fill=text_color, font=font)

        # 更新y坐标
        y_position += text_height + line_height  # 行间距

    return img


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

    async def get_music_alias(self, arg: int = 0) -> None:
        """获取所有曲目别名"""
        if arg == 0:
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
        elif arg == 1:
            try:
                alias_data = await openfile(alias_file)
            except FileNotFoundError:
                alias_data = {}
        else:
            return

        try:
            local_alias_data = await openfile(local_alias_file)
        except FileNotFoundError:
            local_alias_data = {}

        all_alias_data = merge_dicts(alias_data, local_alias_data)

        # # 将字典重构为Alias
        # alias_rebuild: List[Alias] = []
        # for key, values in alias_data.items():
        #     alias_rebuild.append(Alias(id=key, aliases=values))

        self.total_alias_list = AliasList(alias_data=all_alias_data)

mai = MaiMusic()