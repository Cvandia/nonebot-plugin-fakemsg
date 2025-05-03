import re
from typing import Union

from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.plugin import PluginMetadata, get_driver, on_message

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
                "detail_des": (
                    "可使用的命令：\nqq+说+内容|qq+说+内容\n\n例如：\n123456说你好|654321说你好\n\n注意：\n"
                    "1. 伪造消息的qq号必须是机器人好友或者在群内\n"
                    "2. 伪造消息的qq号必须是数字\n"
                    "3. 伪造消息的qq号必须是6-10位\n"
                    "4. 伪造消息的内容不能包含|和说\n"
                    "5. 伪造消息的内容不能超过30个字符\n"
                    "6. 伪造消息的内容不能包含特殊字符\n"
                    "7. 伪造消息的内容不能包含CQ码\n"
                    "8. 伪造消息的内容不能包含空格\n"
                    "9. 伪造消息的内容不能包含换行符\n"
                    "10. 伪造消息的内容不能包含回车符\n"
                    "11. 伪造消息的内容不能包含@",
                ),
            }
        ],
        "menu_template": "default",
    },
)

driver = get_driver()
superusers = driver.config.superusers
whitelist = set(config.fakemsg_whitelist)
user_split = config.user_split
message_split = config.message_split


async def check_if_fakemsg(
    event: Union[GroupMessageEvent, PrivateMessageEvent],
) -> bool:
    if len(event.original_message) > 1 and event.original_message[0].type == "at":
        if event.original_message[1].data.get("text").strip().startswith("说"):
            return True
    elif event.original_message[0].type == "text" and re.match(
        r"^\d{6,10}说", event.original_message[0].data.get("text")
    ):
        return True
    return False


send_fake_msg = on_message(rule=check_if_fakemsg, priority=5, block=True)


@send_fake_msg.handle()
async def _(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent]):
    await send_fake_msg.send("正在伪造消息……")
    fetched_message = event.original_message
    fake_msg_list = []  # 创建伪造消息列表
    at_qq_message = fetched_message["at"]  # 获取at的qq号
    text_message = fetched_message["text"]  # 获取文本消息
    user_index = 0

    for text in text_message:
        raw_text: str = text.data["text"]
        user_msgs = raw_text.split(user_split)
        for raw_user_msg in user_msgs:
            user_msg = raw_user_msg.strip()  # 去除空格
            if user_msg.startswith("说"):
                user_msg = user_msg.split("说", 1)[1]
                user_qq = at_qq_message[user_index].data["qq"]
                user_info = await bot.get_stranger_info(user_id=int(user_qq))
                user_name = user_info["nickname"]
                user_index += 1
            elif user_msg not in {"", " "}:
                try:
                    user_qq, user_msg = user_msg.split("说", 1)
                except ValueError:
                    await send_fake_msg.finish("消息格式错误，缺少“说”。")
            else:
                continue

            # 白名单检测
            if user_qq in whitelist and str(event.user_id) not in superusers:
                await send_fake_msg.finish(f"你没有权限伪造该用户（{user_qq}）的消息。")

            user_info = await bot.get_stranger_info(user_id=int(user_qq))
            user_name = user_info["nickname"]
            fake_msg_list.extend(
                (user_name, user_qq, msg) for msg in user_msg.split(message_split)
            )

    try:
        await send_forward_msg(bot, event, fake_msg_list)
    except Exception as e:
        await send_fake_msg.finish(f"发送失败,{e}")


async def send_forward_msg(
    bot: Bot,
    event: MessageEvent,
    user_message: list[tuple[str, str, Message]],
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

    def to_json(info: tuple[str, str, Message]):
        """
        将消息转换为 forward 消息的 json 格式
        """
        return {
            "type": "node",
            "data": {"name": info[0], "uin": info[1], "content": info[2]},
        }

    messages = [to_json(info) for info in user_message]

    if isinstance(event, GroupMessageEvent):
        await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )
