from enum import Enum, unique
from typing import Dict, List

import httpx
from httpx import Response


##########################################################################################

# 类定义

class HoyoBasicSpider:
    def __init__(self) -> None:
        self.base_url = 'https://bbs-api.mihoyo.com/post/wapi/'  # 基础url
        self.api = None  # api
        self.forum_id = None  # 论坛id
        self.gids = None  # 游戏id
        self.is_good = None  # 是否精品
        self.is_hot = None  # 是否热门
        self.game_name = None  # 游戏名
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.0.0",
            "Referer": "https://bbs.mihoyo.com/",
            "origin": "https://bbs.mihoyo.com",
            "Host": "bbs-api.mihoyo.com",
            "Connection": "keep-alive"
        }

    def get_params(self, page_size: int) -> Dict:
        """获取参数
        :param page_size: 每页数量
        :return: 参数
        """
        pass

    def sync_get_urls(self, page_size: int) -> str:
        """同步获取urls
        :param page_size: 每页数量
        :return: urls
        """
        pass

    def sync_get_name(self, page_size: int) -> str:
        """同步获取names
        :param page_size: 每页数量
        :return: urls
        """
        pass

    def sync_get(self, params: dict = None, is_good: bool = False):
        """同步获取
        :param params: 参数
        :param is_good: 是否精品
        :return: 响应list
        """

        response = httpx.get(self.api, params=params, headers=self.headers)
        return self.handle_response(response, is_good)

    def sync_name(self, params: dict = None, is_good: bool = False):
        """同步获取
        :param params: 参数
        :param is_good: 是否精品
        :return: 响应list
        """

        response = httpx.get(self.api, params=params, headers=self.headers)
        return self.get_rsp_name(response, is_good)

    async def async_get_urls(self, page_size: int = 20) -> List:
        """异步获取urls
        :param page_size: 每页数量
        :return: urls
        """
        pass

    async def async_get_name(self, page_size: int = 20) -> List:
        """异步获取names
        :param page_size: 每页数量
        :return: urls
        """
        pass

    async def async_get(self, params: dict = None, is_good: bool = False):
        """异步获取
        :param params: 参数
        :param is_good: 是否精品
        :return: 响应list
        """

        async with httpx.AsyncClient() as client:
            response = await client.get(self.api, params=params, headers=self.headers)

        return self.handle_response(response, is_good)

    async def async_name(self, params: dict = None, is_good: bool = False):
        """异步获取
        :param params: 参数
        :param is_good: 是否精品
        :return: 响应list
        """

        async with httpx.AsyncClient() as client:
            response = await client.get(self.api, params=params, headers=self.headers)
        return self.get_rsp_name(response, is_good)

    def handle_response(self, response: Response, is_good: bool = False) -> List:
        """处理响应
        :param response: 响应
        :param is_good: 是否精品
        :return: urls list
        """

        urls = []
        if is_good:
            posts = response.json()['data']['posts']
        else:
            posts = response.json()['data']['list']
        for post in posts:
            images = post['post']['images']
            for image in images:
                urls.append(image)
        return urls

    def get_rsp_name(self, response: Response, is_good: bool = False) -> list:
        '''
        获取响应的帖子名称
        '''
        names = []
        if is_good:
            posts = response.json()['data']['posts']
        else:
            posts = response.json()['data']['list']
        for post in posts:
            names.append(post['post']['subject'])
        return names


@unique
class RankType(Enum):
    '''
    排行榜类型
    '''
    Daily = 1  # 日榜
    Weekly = 2  # 周榜
    Monthly = 3  # 月榜


@unique
class LatestType(Enum):
    '''
    最新回复或发帖类型
    '''
    LatestComment = 1  # 最新回复
    LatestPost = 2  # 最新发帖


@unique
class GameType(Enum):
    '''
    游戏类型
    '''
    Genshin = 2  # 原神
    Honkai3rd = 1  # 崩坏3
    DBY = 5  # 大别野
    StarRail = 6  # 星穹铁道
    Honkai2 = 3  # 崩坏2


@unique
class ForumType(Enum):
    '''
    论坛类型
    '''
    GenshinCos = 49  # 原神cos
    GenshinPic = 29  # 原神同人图
    Honkai3rdPic = 4  # 崩坏3同人图
    DBYCOS = 47  # 大别野cos
    DBYPIC = 39  # 大别野同人图
    StarRailPic = 56  # 星穹铁道同人图
    StarRailCos = 62  # 星穹铁道cos
    Honkai2Pic = 40  # 崩坏2同人图
    TearsOfThemisPic = 38  # 泪水同人图


def get_gids(forum: str) -> GameType:
    '''
    根据论坛名获取游戏id
    '''
    forum2gids = {
        'GenshinCos': GameType.Genshin,
        'GenshinPic': GameType.Genshin,
        'Honkai3rdPic': GameType.Honkai3rd,
        'DBYCOS': GameType.DBY,
        'DBYPIC': GameType.DBY,
        'StarRailPic': GameType.StarRail,
        'Honkai2Pic': GameType.Honkai2,
        'StarRailCos': GameType.StarRail,
    }
    return forum2gids[forum]


class Rank(HoyoBasicSpider):
    '''
    排行榜
    url: https://bbs.mihoyo.com/ys/imgRanking/49
    '''

    def __init__(self, forum_id: ForumType, type: RankType) -> None:
        super().__init__()
        self.api = self.base_url + 'getForumPostList'
        self.forum_id = forum_id.value
        gametype = get_gids(forum_id.name)
        self.gids = gametype.value
        self.type = type.value  # 排行榜类型
        self.game_name = gametype.name  # 游戏名

    def get_params(self, page_size: int) -> Dict:
        params = {
            "forum_id": self.forum_id,
            "gids": self.gids,
            "page_size": page_size,
            "type": self.type
        }
        return params

    def sync_get_urls(self, page_size: int = 21) -> List:
        params = self.get_params(page_size)
        return self.sync_get(params)

    async def async_get_urls(self, page_size: int = 21) -> List:
        params = self.get_params(page_size)
        return await self.async_get(params)

    async def async_get_name(self, page_size: int = 21) -> List:
        params = self.get_params(page_size)
        return await self.async_name(params)

    def sync_get_name(self, page_size: int = 21) -> List:
        params = self.get_params(page_size)
        return self.sync_name(params)


class Hot(HoyoBasicSpider):
    '''
    获取热门帖子
    url: https://bbs.mihoyo.com/ys/home/49?type=hot
    '''

    def __init__(self, forum_id: ForumType) -> None:
        super().__init__()
        self.api = self.base_url + 'getForumPostList'
        self.forum_id = forum_id.value
        gametype = get_gids(forum_id.name)
        self.gids = gametype.value
        self.game_name = gametype.name  # 游戏名
        self.is_hot = True

    def get_params(self, page_size: int) -> Dict:
        params = {
            "forum_id": self.forum_id,
            "is_hot": self.is_hot,
            "page_size": page_size
        }
        return params

    def sync_get_urls(self, page_size: int = 20) -> List:
        params = self.get_params(page_size)
        return self.sync_get(params)

    async def async_get_urls(self, page_size: int = 20) -> List:
        params = self.get_params(page_size)
        return await self.async_get(params)

    def sync_get_name(self, page_size: int = 20) -> List:
        params = self.get_params(page_size)
        return self.sync_name(params)

    async def async_get_name(self, page_size: int = 20) -> List:
        params = self.get_params(page_size)
        return await self.async_name(params)


class Good(HoyoBasicSpider):
    '''
    获取精品帖子
    url: https://bbs.mihoyo.com/ys/home/56?type=good
    '''

    def __init__(self, forum_id: ForumType) -> None:
        super().__init__()
        self.api = self.base_url + 'forumGoodPostFullList'
        self.forum_id = forum_id.value
        gametype = get_gids(forum_id.name)
        self.gids = gametype.value
        self.game_name = gametype.name

    def get_params(self, page_size: int) -> Dict:
        params = {
            "forum_id": self.forum_id,
            "gids": self.gids,
            "page_size": page_size
        }
        return params

    def sync_get_urls(self, page_size: int = 20) -> List:
        params = self.get_params(page_size)
        return self.sync_get(params, is_good=True)

    async def async_get_urls(self, page_size: int = 20) -> List:
        params = self.get_params(page_size)
        return await self.async_get(params, is_good=True)

    def sync_get_name(self, page_size: int = 20) -> List:
        params = self.get_params(page_size)
        return self.sync_name(params, is_good=True)

    async def async_get_name(self, page_size: int = 20) -> List:
        params = self.get_params(page_size)
        return await self.async_name(params, is_good=True)


class Latest(HoyoBasicSpider):
    '''
    获取最新回复或发帖
    url: https://bbs.mihoyo.com/ys/home/49?type=1
    '''

    def __init__(self, forum_id: ForumType, type: LatestType) -> None:
        super().__init__()
        self.api = self.base_url + 'getForumPostList'
        self.forum_id = forum_id.value
        gametype = get_gids(forum_id.name)
        self.gids = gametype.value
        self.sort_type = type.value
        self.game_name = gametype.name

    def get_params(self, page_size: int) -> Dict:
        params = {
            "forum_id": self.forum_id,
            "page_size": page_size,
            "sort_type": self.sort_type
        }
        return params

    def sync_get_urls(self, page_size: int = 20) -> List:
        params = self.get_params(page_size)
        return self.sync_get(params)

    async def async_get_urls(self, page_size: int = 20) -> List:
        params = self.get_params(page_size)
        return await self.async_get(params)

    def sync_get_name(self, page_size: int = 20) -> List:
        params = self.get_params(page_size)
        return self.sync_name(params)

    async def async_get_name(self, page_size: int = 20) -> List:
        params = self.get_params(page_size)
        return await self.async_name(params)


# 实例化对象

genshin_rank_daily = Rank(ForumType.GenshinCos, RankType.Daily)
genshin_hot = Hot(ForumType.GenshinCos)
genshin_good = Good(ForumType.GenshinCos)
genshin_latest_comment = Latest(ForumType.GenshinCos, LatestType.LatestComment)

honkai3rd_rank_daily = Rank(ForumType.Honkai3rdPic, RankType.Daily)
honkai3rd_hot = Hot(ForumType.Honkai3rdPic)
honkai3rd_good = Good(ForumType.Honkai3rdPic)
honkai3rd_latest_comment = Latest(ForumType.Honkai3rdPic, LatestType.LatestComment)

dby_rank_daily = Rank(ForumType.DBYPIC, RankType.Daily)
dby_hot = Hot(ForumType.DBYPIC)
dby_good = Good(ForumType.DBYPIC)
dby_latest_comment = Latest(ForumType.DBYPIC, LatestType.LatestComment)

starrail_rank_daily = Rank(ForumType.StarRailCos, RankType.Daily)
starrail_hot = Hot(ForumType.StarRailCos)
starrail_good = Good(ForumType.StarRailCos)
starrail_latest_comment = Latest(ForumType.StarRailCos, LatestType.LatestComment)

honkai2_rank_daily = Rank(ForumType.Honkai2Pic, RankType.Daily)
honkai2_hot = Hot(ForumType.Honkai2Pic)
honkai2_good = Good(ForumType.Honkai2Pic)
honkai2_latest_comment = Latest(ForumType.Honkai2Pic, LatestType.LatestComment)

dbycos_rank_daily = Rank(ForumType.DBYCOS, RankType.Daily)
dbycos_hot = Hot(ForumType.DBYCOS)
dbycos_good = Good(ForumType.DBYCOS)
dbycos_latest_comment = Latest(ForumType.DBYCOS, LatestType.LatestComment)

starrailcos_rank_daily = Rank(ForumType.StarRailCos, RankType.Daily)
starrailcos_hot = Hot(ForumType.StarRailCos)
starrailcos_good = Good(ForumType.StarRailCos)
starrailcos_latest_comment = Latest(ForumType.StarRailCos, LatestType.LatestComment)
