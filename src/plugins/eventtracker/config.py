from typing import List

from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    eventtracker_white_list: List[int]

