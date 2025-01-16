from pydantic import BaseModel, Field
from nonebot import get_plugin_config


class Config(BaseModel):
    """Plugin Config Here"""

    plus_one_priority: int = 10


config = get_plugin_config(Config)