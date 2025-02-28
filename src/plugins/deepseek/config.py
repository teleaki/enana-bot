from typing import List

from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    deepseek_white_list: List[int]
