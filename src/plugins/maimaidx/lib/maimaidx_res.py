from pathlib import Path
from typing import List, Dict


_resource_dir: Path = Path(__file__).parent.parent / 'Resource' / 'static'

alias_file: Path = _resource_dir / 'music_alias.json'                  # 别名暂存文件
local_alias_file: Path = _resource_dir / 'local_music_alias.json'      # 本地别名文件
music_file: Path = _resource_dir / 'music_data.json'                   # 曲目暂存文件
chart_file: Path = _resource_dir / 'music_chart.json'                  # 谱面数据暂存文件

# 静态资源路径
maimai_dir: Path = _resource_dir / 'mai' / 'pic'
cover_dir: Path = _resource_dir / 'mai' / 'cover'
rating_dir: Path = _resource_dir / 'mai' / 'rating'
plate_dir: Path = _resource_dir / 'mai' / 'plate'

# 字体路径
YAHEI: Path = _resource_dir / 'msyh_b.ttf'
MEIRYO: Path =  _resource_dir / 'meiryo.ttc'
SIYUAN: Path = _resource_dir / 'SourceHanSansSC-Bold.otf'
HANYI: Path = _resource_dir / 'HanYi.ttf'
TBFONT: Path = _resource_dir / 'Torus SemiBold.otf'


# 常用变量
SONGS_PER_PAGE: int = 25
scoreRank: List[str] = ['d', 'c', 'b', 'bb', 'bbb', 'a', 'aa', 'aaa', 's', 's+', 'ss', 'ss+', 'sss', 'sss+']
score_Rank: List[str] = ['d', 'c', 'b', 'bb', 'bbb', 'a', 'aa', 'aaa', 's', 'sp', 'ss', 'ssp', 'sss', 'sssp']
score_Rank_l: Dict[str, str] = {'d': 'D', 'c': 'C', 'b': 'B', 'bb': 'BB', 'bbb': 'BBB', 'a': 'A', 'aa': 'AA', 'aaa': 'AAA', 's': 'S', 'sp': 'Sp', 'ss': 'SS', 'ssp': 'SSp', 'sss': 'SSS', 'sssp': 'SSSp'}
comboRank: List[str] = ['fc', 'fc+', 'ap', 'ap+']
combo_rank: List[str] = ['fc', 'fcp', 'ap', 'app']
syncRank: List[str] = ['fs', 'fs+', 'fdx', 'fdx+']
sync_rank: List[str] = ['fs', 'fsp', 'fsd', 'fsdp']
sync_rank_p: List[str] = ['fs', 'fsp', 'fdx', 'fdxp']
diffs: List[str] = ['Basic', 'Advanced', 'Expert', 'Master', 'Re:Master']
levelList: List[str] = ['1', '2', '3', '4', '5', '6', '7', '7+', '8', '8+', '9', '9+', '10', '10+', '11', '11+', '12', '12+', '13', '13+', '14', '14+', '15']
achievementList: List[float] = [50.0, 60.0, 70.0, 75.0, 80.0, 90.0, 94.0, 97.0, 98.0, 99.0, 99.5, 100.0, 100.5]
BaseRaSpp: List[float] = [7.0, 8.0, 9.6, 11.2, 12.0, 13.6, 15.2, 16.8, 20.0, 20.3, 20.8, 21.1, 21.6, 22.4]
fcl: Dict[str, str] = {'fc': 'FC', 'fcp': 'FCp', 'ap': 'AP', 'app': 'APp'}
fsl: Dict[str, str] = {'fs': 'FS', 'fsp': 'FSp', 'fsd': 'FSD', 'fdx': 'FSD', 'fsdp': 'FSDp', 'fdxp': 'FSDp', 'sync': 'Sync'}
ignore_music: List[str] = ['70', '146', '185', '189', '190', '341', '419', '451', '455', '460', '524', '687', '688', '712', '731', '792', '853', '10146', '11213', '11253', '11267']
plate_to_version: Dict[str, str] = {
    '初': 'maimai',
    '真': 'maimai PLUS',
    '超': 'maimai GreeN',
    '檄': 'maimai GreeN PLUS',
    '橙': 'maimai ORANGE',
    '暁': 'maimai ORANGE PLUS',
    '晓': 'maimai ORANGE PLUS',
    '桃': 'maimai PiNK',
    '櫻': 'maimai PiNK PLUS',
    '樱': 'maimai PiNK PLUS',
    '紫': 'maimai MURASAKi',
    '菫': 'maimai MURASAKi PLUS',
    '堇': 'maimai MURASAKi PLUS',
    '白': 'maimai MiLK',
    '雪': 'MiLK PLUS',
    '輝': 'maimai FiNALE',
    '辉': 'maimai FiNALE',
    '熊': 'maimai でらっくす',
    '華': 'maimai でらっくす PLUS',
    '华': 'maimai でらっくす PLUS',
    '爽': 'maimai でらっくす Splash',
    '煌': 'maimai でらっくす Splash PLUS',
    '宙': 'maimai でらっくす UNiVERSE',
    '星': 'maimai でらっくす UNiVERSE PLUS',
    '祭': 'maimai でらっくす FESTiVAL',
    '祝': 'maimai でらっくす FESTiVAL PLUS',
    '双': 'maimai でらっくす BUDDiES'
}
platecn = {
    '晓': '暁',
    '樱': '櫻',
    '堇': '菫',
    '辉': '輝',
    '华': '華'
}
category: Dict[str, str] = {
    '流行&动漫': 'anime',
    '舞萌': 'maimai',
    'niconico & VOCALOID': 'niconico',
    '东方Project': 'touhou',
    '其他游戏': 'game',
    '音击&中二节奏': 'ongeki',
    'POPSアニメ': 'anime',
    'maimai': 'maimai',
    'niconicoボーカロイド': 'niconico',
    '東方Project': 'touhou',
    'ゲームバラエティ': 'game',
    'オンゲキCHUNITHM': 'ongeki',
    '宴会場': '宴会场'
}

charters: List[str] = [
    "-",
    "譜面-100号",
    "ニャイン",
    "maimai TEAM",
    "はっぴー",
    "チャン@DP皆伝",
    "Jack",
    "舞舞10年ズ（チャンとはっぴー）",
    "畳返し",
    "ぴちネコ",
    "mai-Star",
    "rioN",
    "Techno Kitchen",
    "すきやき奉行",
    "合作だよ",
    "某S氏",
    "ものくロシェ",
    "じゃこレモン",
    "小鳥遊さん",
    "Moon Strix",
    "玉子豆腐",
    "ロシェ@ペンギン",
    "シチミヘルツ",
    "原田ひろゆき",
    "Revo@LC",
    "みんなでマイマイマー",
    "しろいろ",
    "サファ太",
    "隅田川星人",
    "華火職人",
    "LabiLabi",
    "如月 ゆかり",
    "ものくろっく",
    "緑風 犬三郎",
    "譜面ボーイズからの挑戦状",
    "Garakuta Scramble!",
    "“H”ack",
    "“H”ack underground",
    "“Carpe diem” ＊ HAN∀BI",
    "小鳥遊さん fused with Phoenix",
    "safaTAmago",
    "JAQ",
    "Phoenix",
    "-ZONE- SaFaRi",
    "PANDORA BOXXX",
    "PANDORA PARADOXXX",
    "ロシアンブラック",
    "翠楼屋",
    "舞舞10年ズ ～ファイナル～",
    "Starlight Disco Festa",
    "鳩ホルダー",
    "みそかつ侍",
    "うさぎランドリー",
    "アマリリス",
    "Redarrow",
    "佑",
    "Luxizhel",
    "ボコ太",
    "7.3Hz＋Jack",
    "シチミッピー",
    "Safata.Hz",
    "7.3GHz vs Phoenix",
    "jacK on Phoenix",
    "KTM",
    "譜面-100号とはっぴー",
    "群青リコリス",
    "いぬっくまとボコっくま",
    "Sukiyaki vs Happy",
    "7.3GHz",
    "ゲキ*チュウマイ Fumen Team",
    "Anomaly Labyrinth",
    "七味星人",
    "しちみりこりす",
    "ﾚよ†ょ／∪ヽ”┠  (十,3､了ﾅﾆ",
    "サファ太 vs -ZONE- SaFaRi",
    "The ALiEN",
    "隅田川華火大会",
    "7.3連発華火",
    "The ALiEN vs. Phoenix",
    "アミノハバキリ",
    "はっぴー respects for 某S氏",
    "さふぁた",
    "小鳥遊さん vs 華火職人",
    "SHICHIMI☆CAT",
    "あまくちジンジャー",
    "Jack & Licorice Gunjyo",
    "超七味星人",
    "一ノ瀬 リズ",
    "-ZONE-Phoenix",
    "KOP3rd with 翡翠マナ",
    "7.3GHz -Før The Legends-",
    "はっぴー星人",
    "Jack & はっぴー vs からめる & ぐるん",
    "maimai Fumen All-Stars",
    "翡翠マナ",
    "チェシャ猫とハートのジャック",
    "カマボコ君",
    "小鳥遊チミ",
    "作譜：翠楼屋",
    "Hz-R.Arrow",
    "ネコトリサーカス団",
    "red phoenix",
    "Redarrow VS 翠楼屋",
    "サファ太 vs じゃこレモン",
    "小鳥遊さん×アミノハバキリ",
    "翠楼屋 vs あまくちジンジャー",
    "たかなっぴー",
    "あまくちヘルツ",
    "サファ太 vs 翠楼屋",
    "アマリリスせんせえ",
    "アマリリスせんせえ with ぴちネコせんせえ",
    "はぴネコ(はっぴー&ぴちネコ)",
    "チャン@DP皆伝 vs シチミヘルツ",
    "メロンポップ",
    "jacK on Phoenix & -ZONE- SaFaRi",
    "PG-NAKAGAWA",
    "Jack vs あまくちジンジャー",
    "翡翠マナ -Memoir-",
    "rintaro soma",
    "DANCE TIME(サファ太)",
    "きょむりん",
    "僕の檸檬本当上手",
    "はっぴー & サファ太",
    "鳩ホルダー & Luxizhel",
    "Safata.GHz",
    "鳩サファzhel",
    "Ruby",
    "ミニミライト",
    "ずんだポップ",
    "maimai TEAM DX",
    "BEYOND THE MEMORiES"
]