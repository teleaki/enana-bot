from pathlib import Path
from typing import List, Dict


_resource_dir: Path = Path(__file__).parent.parent / 'Resource' / 'static'

alias_file: Path = _resource_dir / 'music_alias.json'                  # 别名暂存文件
local_alias_file: Path = _resource_dir / 'local_music_alias.json'      # 本地别名文件
music_file: Path = _resource_dir / 'music_data.json'                   # 曲目暂存文件
chart_file: Path = _resource_dir / 'music_chart.json'                  # 谱面数据暂存文件
user_file: Path = _resource_dir / 'user_diy.json'
guess_rank_file: Path = _resource_dir / 'guess_rank.json'

# 静态资源路径
maimai_dir: Path = _resource_dir / 'mai' / 'pic'
cover_dir: Path = _resource_dir / 'mai' / 'cover'
rating_dir: Path = _resource_dir / 'mai' / 'rating'
plate_dir: Path = _resource_dir / 'mai' / 'plate'
other_plate_dir: Path = _resource_dir / 'mai' / 'other_plate'

# 字体路径
YAHEI: Path = _resource_dir / 'msyh_b.ttf'
MEIRYO: Path =  _resource_dir / 'meiryo.ttc'
SIYUAN: Path = _resource_dir / 'SourceHanSansSC-Bold.otf'
HANYI: Path = _resource_dir / 'HanYi.ttf'
TBFONT: Path = _resource_dir / 'Torus SemiBold.otf'
SATISFY: Path = _resource_dir / 'Satisfy.ttf'


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
plate_to_version_cn: Dict[str, str] = {
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
    '華': 'maimai でらっくす',
    '华': 'maimai でらっくす',
    '爽': 'maimai でらっくす Splash',
    '煌': 'maimai でらっくす Splash',
    '宙': 'maimai でらっくす UNiVERSE',
    '星': 'maimai でらっくす UNiVERSE',
    '祭': 'maimai でらっくす FESTiVAL',
    '祝': 'maimai でらっくす FESTiVAL',
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

real_charters: Dict[str, List[str]] = {
    "譜面-100号": ["譜面-100号", "譜面-100号とはっぴー"],
    "ニャイン": ["ニャイン"],
    "はっぴー": ["はっぴー", "舞舞10年ズ（チャンとはっぴー）", "原田ひろゆき", "みんなでマイマイマー", "緑風 犬三郎", "シチミッピー", "譜面-100号とはっぴー", "いぬっくまとボコっくま", "Sukiyaki vs Happy", "はっぴー respects for 某S氏", "はっぴー星人", "Jack & はっぴー vs からめる & ぐるん", "チェシャ猫とハートのジャック", "たかなっぴー", "はぴネコ(はっぴー&ぴちネコ)", "はっぴー & サファ太"],
    "チャン@DP皆伝": ["チャン@DP皆伝", "舞舞10年ズ（チャンとはっぴー）", "Garakuta Scramble!", "舞舞10年ズ ～ファイナル～", "チャン@DP皆伝 vs シチミヘルツ"],
    "Jack": ["Jack", "Garakuta Scramble!", "“H”ack", "“H”ack underground", "JAQ", "7.3Hz＋Jack", "jacK on Phoenix", "Jack & Licorice Gunjyo", "Jack & はっぴー vs からめる & ぐるん", "jacK on Phoenix & -ZONE- SaFaRi", "Jack vs あまくちジンジャー"],
    "畳返し": ["畳返し"],
    "ぴちネコ": ["ぴちネコ", "ロシアンブラック", "SHICHIMI☆CAT", "チェシャ猫とハートのジャック", "アマリリスせんせえ with ぴちネコせんせえ", "はぴネコ(はっぴー&ぴちネコ)"],
    "mai-Star": ["mai-Star"],
    "rioN": ["rioN"],
    "Techno Kitchen": ["Techno Kitchen"],
    "すきやき奉行": ["すきやき奉行", "Sukiyaki vs Happy"],
    "某S氏": ["某S氏"],
    "じゃこレモン": ["じゃこレモン", "サファ太 vs じゃこレモン", "僕の檸檬本当上手"],
    "小鳥遊さん": ["小鳥遊さん", "小鳥遊さん fused with Phoenix", "Phoenix", "7.3GHz vs Phoenix", "jacK on Phoenix", "The ALiEN vs. Phoenix", "小鳥遊さん vs 華火職人", "-ZONE-Phoenix", "小鳥遊チミ", "red phoenix", "小鳥遊さん×アミノハバキリ", "jacK on Phoenix & -ZONE- SaFaRi"],
    "Moon Strix": ["Moon Strix"],
    "玉子豆腐": ["玉子豆腐", "safaTAmago"],
    "ロシェ@ペンギン": ["ロシェ@ペンギン", "ものくロシェ"],
    "シチミヘルツ": ["シチミヘルツ", "7.3Hz＋Jack", "シチミッピー", "Safata.Hz", "7.3GHz vs Phoenix", "7.3GHz", "七味星人", "しちみりこりす", "7.3連発華火", "SHICHIMI☆CAT", "超七味星人", "7.3GHz -Før The Legends-", "Hz-R.Arrow", "あまくちヘルツ", "チャン@DP皆伝 vs シチミヘルツ", "Safata.GHz"],
    # 7.3GHz更常用遂加
    "7.3GHz": ["シチミヘルツ", "7.3Hz＋Jack", "シチミッピー", "Safata.Hz", "7.3GHz vs Phoenix", "7.3GHz", "七味星人", "しちみりこりす", "7.3連発華火", "SHICHIMI☆CAT", "超七味星人", "7.3GHz -Før The Legends-", "Hz-R.Arrow", "あまくちヘルツ", "チャン@DP皆伝 vs シチミヘルツ", "Safata.GHz"],
    "Revo@LC": ["Revo@LC"],
    "サファ太": ["サファ太", "safaTAmago", "-ZONE- SaFaRi", "ボコ太", "Safata.Hz", "ﾚよ†ょ／∪ヽ”┠  (十,3､了ﾅﾆ", "サファ太 vs -ZONE- SaFaRi", "さふぁた", "-ZONE-Phoenix", "サファ太 vs じゃこレモン", "サファ太 vs 翠楼屋", "jacK on Phoenix & -ZONE- SaFaRi", "DANCE TIME(サファ太)", "はっぴー & サファ太", "Safata.GHz", "鳩サファzhel"],
    "隅田川星人": ["隅田川星人", "七味星人", "The ALiEN", "隅田川華火大会", "The ALiEN vs. Phoenix", "超七味星人", "はっぴー星人"],
    "華火職人": ["華火職人", "“Carpe diem” ＊ HAN∀BI", "ﾚよ†ょ／∪ヽ”┠  (十,3､了ﾅﾆ", "隅田川華火大会", "7.3連発華火", "小鳥遊さん vs 華火職人"],
    "LabiLabi": ["LabiLabi"],
    "如月 ゆかり": ["如月 ゆかり"],
    "ものくろっく": ["ものくろっく", "ものくロシェ"],
    "翠楼屋": ["翠楼屋", "KOP3rd with 翡翠マナ", "翡翠マナ", "作譜：翠楼屋", "Redarrow VS 翠楼屋", "翠楼屋 vs あまくちジンジャー", "サファ太 vs 翠楼屋", "翡翠マナ -Memoir-", "Ruby"],
    "鳩ホルダー": ["鳩ホルダー", "鳩ホルダー & Luxizhel", "鳩サファzhel"],
    "みそかつ侍": ["みそかつ侍"],
    "うさぎランドリー": ["うさぎランドリー"],
    "アマリリス": ["アマリリス", "アマリリスせんせえ", "アマリリスせんせえ with ぴちネコせんせえ",],
    "Redarrow": ["Redarrow", "Hz-R.Arrow", "red phoenix", "Redarrow VS 翠楼屋"],
    "佑": ["佑"],
    "Luxizhel": ["Luxizhel", "鳩ホルダー & Luxizhel", "鳩サファzhel"],
    "KTM": ["KTM"],
    "群青リコリス": ["群青リコリス", "しちみりこりす", "Jack & Licorice Gunjyo"],
    "アミノハバキリ": ["アミノハバキリ", "小鳥遊さん×アミノハバキリ"],
    "あまくちジンジャー": ["あまくちジンジャー", "翠楼屋 vs あまくちジンジャー", "あまくちヘルツ", "Jack vs あまくちジンジャー"],
    "カマボコ君": ["カマボコ君", "いぬっくまとボコっくま", "ボコ太", "小鳥遊チミ"],
    "メロンポップ": ["メロンポップ", "ずんだポップ"],
    "PG-NAKAGAWA": ["PG-NAKAGAWA"],
    "rintaro soma": ["rintaro soma"],
    "きょむりん": ["きょむりん"],
    "ミニミライト": ["ミニミライト"],
# 显然是马甲但是不确定或太复杂或谱师团建懒得加
    "maimai TEAM":["maimai TEAM"],
    "合作だよ":["合作だよ"],
    "しろいろ":["しろいろ"],
    "譜面ボーイズからの挑戦状": ["譜面ボーイズからの挑戦状"],
    "PANDORA BOXXX": ["PANDORA BOXXX"],
    "PANDORA PARADOXXX": ["PANDORA PARADOXXX"],
    "舞舞10年ズ ～ファイナル～": ["舞舞10年ズ ～ファイナル～"],
    "Starlight Disco Festa": ["Starlight Disco Festa"],
    "ゲキ*チュウマイ Fumen Team": ["ゲキ*チュウマイ Fumen Team"],
    "Anomaly Labyrinth": ["Anomaly Labyrinth"],
    "一ノ瀬 リズ": ["一ノ瀬 リズ"],
    "maimai Fumen All-Stars": ["maimai Fumen All-Stars"],
    "ネコトリサーカス団": ["ネコトリサーカス団"],
    "maimai TEAM DX": ["maimai TEAM DX"],
    "BEYOND THE MEMORiES": ["BEYOND THE MEMORiES"]
}
