from typing import List

from nonebot.plugin import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    user_split: str = "|"
    message_split: str = " "
    fakemsg_whitelist: List[str] = []


config = get_plugin_config(Config)
