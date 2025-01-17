from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment

from pathlib import Path
import random, json

class GettingManager:
    def __init__(self):
        self._eating_path : Path = Path(__file__).parent / "resource" / "food.json"
        self._drinking_path : Path = Path(__file__).parent / "resource" / "drinks.json"

    def _load_food_json(self):
        try:
            with open(self._eating_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError as e:
            return FileNotFoundError(f"未找到food.json文件: {e}")
        except json.JSONDecodeError as e:
            return json.JSONDecodeError(f"food.json解析失败: {e}")

    def get_food(self):
        data = self._load_food_json()

        # 判断返回的是否为异常对象
        if isinstance(data, FileNotFoundError):
            return Message(MessageSegment.text(str(data)))  # 显示错误消息
        elif isinstance(data, json.JSONDecodeError):
            return Message(MessageSegment.text(str(data)))  # 显示错误消息

        if data:
            # 随机选择一种食物
            choice = random.choice(data['food'])
            msg = Message([
                MessageSegment.text("enana建议你吃：\n"),
                MessageSegment.text(f"✨{choice['name']}✨\n"),
                MessageSegment.image(choice['url'])  # 如果需要显示图片，取消注释
            ])
        else:
            msg = Message(MessageSegment.text("菜谱为空,只能饿肚子了😭"))

        return msg

    def _load_drink_json(self):
        try:
            with open(self._drinking_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError as e:
            return FileNotFoundError(f"未找到drinks.json文件: {e}")
        except json.JSONDecodeError as e:
            return json.JSONDecodeError(f"drinks.json解析失败: {e}")

    def get_drink(self):
        data = self._load_drink_json()

        # 判断返回的是否为异常对象
        if isinstance(data, FileNotFoundError):
            return Message(MessageSegment.text(str(data)))  # 显示错误消息
        elif isinstance(data, json.JSONDecodeError):
            return Message(MessageSegment.text(str(data)))  # 显示错误消息

        if data:
            # 随机选择一个店名
            brand_choice = random.choice(list(data['drinks'].keys()))  # 随机选择店名
            # 获取该店的饮品列表
            drink_list = data['drinks'][brand_choice]
            # 随机选择一个饮品
            item_choice = random.choice(drink_list)
            msg = Message([
                MessageSegment.text("enana建议你喝：\n"),
                MessageSegment.text(f"🎈{brand_choice}🎈的✨{item_choice['name']}✨\n"),
                MessageSegment.image(item_choice['url'])  # 如果需要显示图片，取消注释
            ])
        else:
            msg = Message(MessageSegment.text("菜谱为空,只能渴着了😭"))

        return msg

eord_manager = GettingManager()
