from nonebot.adapters.onebot.v11 import (
    Message,
    MessageEvent,
    Bot,
    GroupMessageEvent,
    PrivateMessageEvent,
)
import re, httpx
from typing import List, Tuple, Union, Any
from nonebot.plugin import on_message, PluginMetadata
from .config import Config, config

__plugin_meta__ = PluginMetadata(
    name="消息伪造",
    description="伪造消息",
    usage="qq+说+内容|qq+说+内容",
    config=Config,
    type="application",
    homepage="https://github.com/Cvandia/nonebot-plugin-fakemsg",
    supported_adapters={"~onebot.v11"},
    extra={
        "menu_data": [
            {
                "func": "伪造消息",
                "trigger_method": "on_message",
                "trigger_condition": "暂无介绍",
                "brief_des": "用于伪造恶搞群友或者好友的消息",
                "detail_des": "可使用的命令：\nqq+说+内容|qq+说+内容\n\n例如：\n123456说你好|654321说你好\n\n注意：\n1. 伪造消息的qq号必须是机器人好友或者在群内\n2. 伪造消息的qq号必须是数字\n3. 伪造消息的qq号必须是6-10位\n4. 伪造消息的内容不能包含|和说\n5. 伪造消息的内容不能超过30个字符\n6. 伪造消息的内容不能包含特殊字符\n7. 伪造消息的内容不能包含CQ码\n8. 伪造消息的内容不能包含空格\n9. 伪造消息的内容不能包含换行符\n10. 伪造消息的内容不能包含回车符\n11. 伪造消息的内容不能包含@",
            }
        ],
        "menu_template": "default",
    },
)

user_split = config.user_split
message_split = config.message_split


async def check_if_fakemsg(
    bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent]
) -> bool:
    """
    检查是否为伪造消息

    > 参数：
        - bot: Bot 对象
        - event: MessageEvent 对象

    > 返回值：
        - 是伪造消息：True
        - 不是伪造消息：False
    """
    if event.original_message[0].type == "at":
        if event.original_message[1].data["text"].strip().startswith("说"):
            return True
    elif event.original_message[0].type == "text":
        if re.match(r"^\d{6,10}说", event.original_message[0].data["text"]):
            return True
    return False


send_fake_msg = on_message(rule=check_if_fakemsg, priority=5, block=True)


@send_fake_msg.handle()
async def _(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent]):
    await send_fake_msg.send("正在伪造消息……")
    raw_message = event.raw_message
    fake_msg_list = []
    user_msgs = raw_message.split(user_split)
    for user_msg in user_msgs:
        qq_msg = user_msg.split("说", 1)[0].strip()
        if qq_msg.isdigit():
            qq = qq_msg
        else:
            matches = re.match(r"^\[CQ:at,qq=(\d{6,10})\]", qq_msg)
            if matches:
                qq = matches.group(1)
            else:
                qq = bot.self_id
                await send_fake_msg.finish("无法正确识别at信息", at_sender=True)
        msgs = user_msg.split("说", 1)[1].split(message_split)
        try:
            name = await bot.get_stranger_info(user_id=int(qq))
            name = name["nickname"]
        except:
            res = httpx.get("https://api.usuuu.com/qq/{}".format(qq))
            data = res.json()
            name = data.get("data").get("name")
        for msg in msgs:
            fake_msg_list.append((name, qq, Message(msg)))
    await send_forward_msg(bot, event, fake_msg_list)


async def send_forward_msg(
    bot: Bot,
    event: MessageEvent,
    user_message: List[Tuple[str, str, Message]],
):
    """
    发送 forward 消息

    > 参数：
        - bot: Bot 对象
        - event: MessageEvent 对象
        - user_message: 合并消息的用户信息列表

    > 返回值：
        - 成功：返回消息发送结果
        - 失败：抛出异常
    """

    def to_json(info: Tuple[str, str, Message]):
        """
        将消息转换为 forward 消息的 json 格式
        """
        return {
            "type": "node",
            "data": {"name": info[0], "uin": info[1], "content": info[2]},
        }

    messages = [to_json(info) for info in user_message]
    if isinstance(event, GroupMessageEvent):
        return await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        return await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )
