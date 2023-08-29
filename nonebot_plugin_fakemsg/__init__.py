from nonebot.adapters.onebot.v11 import (
    Message,
    MessageEvent,
    Bot,
    GroupMessageEvent,
    PrivateMessageEvent,
)
import re
from typing import List, Union
from nonebot.plugin import on_regex, PluginMetadata
from nonebot.params import RegexStr
from .config import config

__plugin_meta__ = PluginMetadata(
    name="消息伪造",
    description="伪造消息",
    usage="qq+说+内容|qq+说+内容",
    config=config,
    type="application",
    homepage="https://github.com/Cvandia/nonebot-plugin-fakemsg",
    supported_adapters={"~onebot.v11"},
    extra={
        "menu_data": [
            {
                "func": "伪造消息",
                "trigger_method": "on_regex",
            }
        ],
        "menu_template": "default",
    },
)

user_split = config.user_split
message_split = config.message_split

send_fake_msg = on_regex(r"^(\d{6,10})说(.*)", flags=re.I, priority=5, block=False)


@send_fake_msg.handle()
async def _(
    bot: Bot,
    event: Union[PrivateMessageEvent, GroupMessageEvent],
    args: str = RegexStr(),
):
    await send_fake_msg.send(f"正在伪造消息...")
    fake_msg_list = []
    users_msgs = args.split(user_split)
    for user_msg in users_msgs:
        try:
            qq = user_msg.split("说", 1)[0]  # 以 ‘说’ 为分隔qq号和消息内容
            msgs = user_msg.split("说", 1)[1].split(message_split)  # 以空格为分隔消息内容和消息内容
        except IndexError:
            await send_fake_msg.finish("消息格式错误")
        try:
            res = await bot.get_stranger_info(user_id=qq)
        except Exception as e:
            await send_fake_msg.finish(f"获取用户信息失败{e},请检查qq号是否正确")
        name = res["nickname"]
        for msg in msgs:
            fake_msg_list.append((name, qq, msg))
    try:
        await send_forward_msg(bot, event, fake_msg_list)
    except Exception as e:
        await send_fake_msg.finish(f"发送失败{e}")


async def send_forward_msg(
    bot: Bot,
    event: MessageEvent,
    msgs: List[Message],
) -> dict:
    """
    发送 forward 消息

    > 参数：
        - bot: Bot 对象
        - event: MessageEvent 对象
        - msgs: 消息列表

    > 返回值：
        - 成功：返回消息发送结果
        - 失败：抛出异常
    """

    def to_json(msg):
        return {
            "type": "node",
            "data": {"name": msg[0], "uin": msg[1], "content": msg[2]},
        }

    messages = [to_json(msg) for msg in msgs]
    if isinstance(event, GroupMessageEvent):
        return await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        return await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )
