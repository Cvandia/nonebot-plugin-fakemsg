from pydantic import Extra, BaseModel
from nonebot import get_driver


class Config(BaseModel, extra=Extra.ignore):
    fake_split: str = "|"

config = Config.parse_obj(get_driver().config.dict())
