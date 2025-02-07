from typing import Any, List, Optional, Union

import httpx

from .maimaidx_error import *


class MaiAPI:
    def __init__(self):
        self.Diving_fish = 'https://www.diving-fish.com/api/maimaidxprober'
        self.Xray_alias = 'https://download.fanyu.site/maimai/alias.json'
        self.QQ_logo = 'http://q1.qlogo.cn/g'

    async def _request(self, method: str, url: str, **kwargs) -> Any:
        session = httpx.AsyncClient(timeout=30)
        res = await session.request(method, url, **kwargs)

        data = None

        if self.Diving_fish in url:
            if res.status_code == 200:
                data = res.json()
            elif res.status_code == 400:
                raise UserNotFoundError
            elif res.status_code == 403:
                raise UserDisabledQueryError
            else:
                raise UnknownError

        if self.Xray_alias in url:
            if res.status_code == 200:
                data = res.json()
            elif res.status_code == 400:
                raise UserNotFoundError
            elif res.status_code == 403:
                raise UserDisabledQueryError
            else:
                raise UnknownError

        elif self.QQ_logo in url:
            if res.status_code == 200:
                data = res.content
            else:
                raise

        await session.aclose()
        return data

    async def music_data(self):
        """获取曲目数据"""
        return await self._request('GET', self.Diving_fish + '/music_data')

    async def chart_stats(self):
        """获取单曲数据"""
        return await self._request('GET', self.Diving_fish + '/chart_stats')

    async def music_alias(self):
        """获取别名数据"""
        return await self._request('GET', self.Xray_alias)

    async def query_user(self, project: str, *, qqid: Optional[int] = None, username: Optional[str] = None,
                         version: Optional[List[str]] = None):
        """
        请求用户数据
        - `project`: 查询的功能
            - `player`: 查询用户b50
            - `plate`: 按版本查询用户游玩成绩
        - `qqid`: 用户QQ
        - `username`: 查分器用户名
        """
        json = {}
        if qqid:
            json['qq'] = qqid
        if username:
            json['username'] = username
        if version:
            json['version'] = version
        if project == 'player':
            json['b50'] = True
        return await self._request('POST', self.Diving_fish + f'/query/{project}', json=json)

    async def qq_logo(self, qqid: Union[int, str]):
        params = {
            'b': 'qq',
            'nk': qqid,
            's': 100
        }
        return await self._request('GET', self.QQ_logo, params=params)

maiapi = MaiAPI()