from pydantic import BaseModel
from typing import Optional, Dict, List

class Config(BaseModel):
    """Plugin Config Here"""

oc_dict: Dict[str, str] = {
    'ick': '001', 'saki': '002', 'hnm': '003', 'shiho': '004',
    'mnr': '005', 'hrk': '006', 'airi': '007', 'szk': '008',
    'khn': '009', 'an': '010', 'akt': '011', 'toya': '012',
    'tks': '013', 'emu': '014', 'nene': '015', 'rui': '016',
    'knd': '017', 'mfy': '018', 'ena': '019', 'mzk': '020',
    'miku': '021', 'rin': '022', 'len': '023', 'luka': '024',
    'meiko': '025', 'kaito': '026'
}
oc_name: Dict[str, str] = {
    'ick': '星乃一歌', 'saki': '天马咲希', 'hnm': '望月穗波', 'shiho': '日森野志步',
    'mnr': '花里实乃理', 'hrk': '桐谷遥', 'airi': '桃井爱莉', 'szk': '日森野雫',
    'khn': '小豆沢心羽', 'an': '白石杏', 'akt': '东云彰人', 'toya': '青柳冬弥',
    'tks': '天马司', 'emu': '凤笑梦', 'nene': '草薙宁宁', 'rui': '神代类',
    'knd': '宵崎奏', 'mfy': '朝比奈真冬', 'ena': '东云绘名', 'mzk': '晓山瑞希',
    'miku': '初音未来', 'rin': '镜音铃', 'len': '镜音连', 'luka': '巡音流歌',
    'meiko': 'MEIKO', 'kaito': 'KAITO'
}
card_type: List[str] = ["card_normal", "card_after_training"]