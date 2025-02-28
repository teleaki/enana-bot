from typing import List

from pydantic import BaseModel


class ScopedConfig(BaseModel):
    white_list: List[str]
    black_list: List[str]

class Config(BaseModel):
    """Plugin Config Here"""
    mai_total: ScopedConfig
    mai_guess: ScopedConfig
