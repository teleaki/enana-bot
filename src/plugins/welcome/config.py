from pydantic import BaseModel
from typing import List


class Config(BaseModel):
    """Plugin Config Here"""
    welcome_black_list: List[int]
