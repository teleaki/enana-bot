from pydantic import BaseModel

class Config(BaseModel):
    """Plugin Config Here"""
    oc_dict = {
        'ick': '001',  'saki': '002', 'hnm': '003',  'shiho': '004',
        'mnr': '005',  'hrk': '006',  'airi': '007', 'szk': '008',
        'khn': '009',  'an': '010',   'akt': '011',  'toya': '012',
        'tks': '013',  'emu': '014',  'nene': '015', 'rui': '016',
        'knd': '017',  'mfy': '018',  'ena': '019',  'mzk': '020',
        'miku': '021', 'rin': '022',  'len': '023',  'luka': '024', 'meiko': '025', 'kaito': '026'
    }
    oc_num_dict = {
        'ick': 39, 'saki': 43, 'hnm': 42, 'shiho': 44,
        'mnr': 40, 'hrk': 42, 'airi': 41, 'szk': 41,
        'khn': 41, 'an': 41, 'akt': 44, 'toya': 42,
        'tks': 41, 'emu': 42, 'nene': 40, 'rui': 41,
        'knd': 41, 'mfy': 41, 'ena': 42, 'mzk': 40,
        'miku': 52, 'rin': 42, 'len': 44, 'luka': 43, 'meiko': 43, 'kaito': 45
    }
    card_type = [
        "card_normal", "card_after_training"
    ]