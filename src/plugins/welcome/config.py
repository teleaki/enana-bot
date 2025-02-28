from pydantic import BaseModel
from typing import List


class ScopedConfig(BaseModel):
    white_list: List[int]
    black_list: List[int]

    def is_blacklisted(self, user: int) -> bool:
        return user in self.black_list

    def is_whitelisted(self, user: int) -> bool:
        return user in self.white_list


class Config(BaseModel):
    """Plugin Config Here"""
    welcome: ScopedConfig
