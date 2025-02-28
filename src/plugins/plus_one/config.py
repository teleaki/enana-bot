from typing import List

from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    plus_one_black_list: List[int]
