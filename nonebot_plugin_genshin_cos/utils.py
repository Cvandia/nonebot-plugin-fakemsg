from asyncio import sleep
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

import httpx
from httpx import TimeoutException
from nonebot import get_driver
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message, GROUP_ADMIN, GROUP_OWNER
from nonebot.exception import ActionFailed
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER

from .config import Config

#######################################################

# 拓展的异常类和函数
SUPER_PERMISSION = GROUP_ADMIN | GROUP_OWNER | SUPERUSER
GENSHIN_NAME = ["原神", 'OP', 'op', '欧泡', '⭕', '🅾️', '🅾️P', '🅾️p', '原', '圆']
HONKAI3RD_NAME = ['崩坏3', '崩崩崩', '蹦蹦蹦', '崩坏三', '崩三', '崩崩崩三', '崩坏3rd', '崩坏3Rd', '崩坏3RD', '崩坏3rd',
                  '崩坏3RD', '崩坏3Rd']
DBY_NAME = ['大别野', 'DBY', 'dby']
STAR_RAIL = ['星穹铁道', '星穹', '崩铁', '铁道', '星铁', '穹p', '穹铁']


class WriteError(Exception):
    """写入错误"""
    pass


# 加载配置

MAX = Config.parse_obj(get_driver().config.dict()).cos_max
SAVE_PATH = Path(Config.parse_obj(get_driver().config.dict()).cos_path)
CD = Config.parse_obj(get_driver().config.dict()).cos_cd
DELAY = Config.parse_obj(get_driver().config.dict()).cos_delay
IS_FORWARD = Config.parse_obj(get_driver().config.dict()).cos_forward_msg


def check_cd(user_id: int, user_data: Dict[str, datetime]) -> Tuple[bool, int, dict]:
    """检查用户触发事件的cd

    Args:
        user_id (int): 用户的id
        user_data (dict): 用户数据

    Returns:
        Tuple[bool,int,dict]: 返回一个元组，第一个元素为True表示可以触发，为False表示不可以触发，第二个元素为剩余时间，第三个元素为用户数据
    """
    data = user_data
    if str(user_id) not in data:
        data[str(user_id)] = datetime.now()
    if datetime.now() < data[f'{user_id}']:
        delta = (data[str(user_id)] - datetime.now()).seconds
        return False, delta, data
    else:
        data[str(user_id)] = datetime.now() + timedelta(seconds=CD)
        return True, 0, data


async def download_from_urls(urls: List[str], path: Path):
    '''
    下载图片
    :param urls: 图片链接
    :param path: 保存路径
    :return: None
    '''
    is_download_error = False
    error_cnt = 0
    success_cnt = 0
    if not path.exists():
        path.mkdir(parents=True)
    if not path.is_dir():
        raise WriteError('路径不是文件夹')
    async with httpx.AsyncClient() as client:
        for url in urls:
            try:
                filename = url.split('/')[-1]
                new_path = path / filename
                rsp = await client.get(url)
                content = rsp.content
                with open(new_path, 'wb') as f:
                    f.write(content)
            except (httpx.ConnectError, httpx.RequestError, httpx.ReadTimeout, TimeoutException):
                is_download_error = True
                error_cnt += 1
                continue
            if is_download_error:
                raise WriteError(f'有{error_cnt}张图片由于超时下载失败了')
            success_cnt += 1
            logger.success(f'下载{success_cnt}张成功')


async def send_forward_msg(
        bot: Bot,
        event: MessageEvent,
        name: str,
        uin: str,
        msgs: list,
) -> dict:
    """调用合并转发API

    params:
        bot: Bot,
        event: 消息事件类型,
        name: 发送者昵称,
        uin: 发送者账号,
        msgs: 消息列表,
    """

    def to_json(msg: Message):
        return {"type": "node", "data": {"name": name, "uin": uin, "content": msg}}

    messages = [to_json(msg) for msg in msgs]

    if isinstance(event, GroupMessageEvent):
        return await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        return await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )


def msglist2forward(name: str, uin: str, msgs: list) -> list:
    """调用合并转发群API

    params:
        bot: Bot
        name: 发送者昵称
        uin: 发送者账号
        msgs: 消息列表
    """

    def to_json(msg: Message):
        return {"type": "node", "data": {"name": name, "uin": uin, "content": msg}}

    return [to_json(msg) for msg in msgs]


async def send_regular_msg(matcher: Matcher, messages: list):
    '''
    发送常规消息
    :param matcher: Matcher
    :param messages: 消息列表
    '''
    cnt = 1
    for msg in messages:
        try:
            cnt += 1
            await matcher.send(msg)
            await sleep(DELAY)
        except ActionFailed:
            if cnt <= 2:
                await matcher.send('消息可能风控,请尝试更改为合并转发模式')
