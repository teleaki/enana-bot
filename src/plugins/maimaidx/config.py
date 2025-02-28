from typing import List

from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    mai_query_black_list: List[int]
    mai_guess_white_list: List[int]
