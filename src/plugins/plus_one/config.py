from typing import List

from pydantic import BaseModel


class ScopedConfig(BaseModel):
    white_list: List[int]
    black_list: List[int]

    def is_blacklisted(self, user: int) -> bool:
        return user in self.black_list

    def is_whitelisted(self, user: int) -> bool:
        return user in self.white_list

class Config(BaseModel):
    """Plugin Config Here"""
    plusone: ScopedConfig
