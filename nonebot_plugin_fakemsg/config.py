from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    user_split: str = "|"
    message_split: str = " "


config = Config.parse_obj(get_driver().config.dict())
