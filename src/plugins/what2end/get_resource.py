from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment

import random, json

class GettingManager:
    def __init__(self):
        self._eating_path = 'resource/food.json'
        self._drinking_path = 'resource/drinks.json'

    def _load_food_json(self):
        try:
            with open(self._eating_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return e

    def get_food(self):
        data = self._load_food_json()
        if data:
            if isinstance(data, FileNotFoundError):  # 检查是否为FileNotFoundError异常对象
                return Message(MessageSegment.text("未能读取菜谱: 未找到food.json"))
            elif isinstance(data, json.JSONDecodeError):  # 检查是否为JSONDecodeError异常对象
                return Message(MessageSegment.text("未能读取菜谱: food.json解析失败"))

            # 随机选择一种食物
            choice = random.choice(data['food'])
            msg = Message([
                MessageSegment.text("enana建议你吃：\n"),
                MessageSegment.text(f"✨{choice['name']}✨\n"),
                # MessageSegment.image(choice['url'])
            ])
        else:
            msg = Message(MessageSegment.text("菜谱为空,只能饿肚子了😭"))
        return msg

    def _load_drink_json(self):
        try:
            with open(self._drinking_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return e

    def get_drink(self):
        data = self._load_drink_json()
        if data:
            if isinstance(data, FileNotFoundError):  # 检查是否为FileNotFoundError异常对象
                return Message(MessageSegment.text("未能读取菜谱: 未找到drinks.json"))
            elif isinstance(data, json.JSONDecodeError):  # 检查是否为JSONDecodeError异常对象
                return Message(MessageSegment.text("未能读取菜谱: drinks.json解析失败"))

            # 随机选择一个店名
            brand_choice = random.choice(list(data['drinks'].keys()))  # 随机选择店名
            # 获取该店的饮品列表
            drink_list = data['drinks'][brand_choice]
            # 随机选择一个饮品
            item_choice = random.choice(drink_list)
            msg = Message([
                MessageSegment.text("enana建议你喝：\n"),
                MessageSegment.text(f"🎈{brand_choice}🎈的✨{item_choice['name']}✨\n"),
                # MessageSegment.image(item_choice['url'])
            ])
        else:
            msg = Message(MessageSegment.text("菜谱为空,只能渴着了😭"))
        return msg

eord_manager = GettingManager()
