from pydantic import BaseModel
from typing import Optional, Dict, List, Tuple


class ChartInfo(BaseModel):
    achievements: float
    ds: float
    dxScore: int
    fc: Optional[str] = ''
    fs: Optional[str] = ''
    level: str
    level_index: int
    level_label: str
    ra: int
    rate: str
    song_id: int
    title: str
    type: str


class Data(BaseModel):
    sd: Optional[List[ChartInfo]] = None
    dx: Optional[List[ChartInfo]] = None


class UserInfo(BaseModel):
    additional_rating: Optional[int]
    charts: Optional[Data]
    nickname: Optional[str]
    plate: Optional[str] = None
    rating: Optional[int]
    username: Optional[str]
