from nonebot.adapters.onebot.v11 import Message, MessageSegment

from .get_resource import eord_manager

import json

def menu_show():
    try:
        food_data = eord_manager.load_food_json()
        drinks_data = eord_manager.load_drinks_json()
    except (FileNotFoundError, json.JSONDecodeError) as e:
        # 捕获文件读取或 JSON 解码异常，返回错误信息
        return Message(MessageSegment.text(f"发生错误: {str(e)}"))

    # 菜品部分
    food_msg = Message("菜品：\n")
    for food in food_data.get("food", []):
        food_msg.append(f"  ● {food['name']}\n")

    # 饮品部分
    drinks_msg = Message("饮品：\n")
    for drinks_brand, drinks_list in drinks_data.get('drinks', {}).items():
        drinks_msg.append(f" - {drinks_brand}：\n")
        for drink_item in drinks_list:
            drinks_msg.append(f"  ● {drink_item['name']}\n")

    # 合并菜品和饮品的消息
    return [food_msg, drinks_msg]
