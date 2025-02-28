from typing import List

from pydantic import BaseModel

from pydantic import BaseModel
from typing import List


class ScopedConfig(BaseModel):
    whitelist: List[str]
    blacklist: List[str]

    def is_blacklisted(self, user: int) -> bool:
        return user in self.blacklist

    def is_whitelisted(self, user: int) -> bool:
        return user in self.whitelist


class Config(BaseModel):
    """Plugin Config Here"""
    welcome: ScopedConfig
