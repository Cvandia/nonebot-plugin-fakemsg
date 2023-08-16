from random import choice
from typing import Annotated

from nonebot import get_bot
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.params import RegexGroup, ArgPlainText, CommandArg, CommandStart
from nonebot.plugin import on_regex, on_command, require, PluginMetadata
from nonebot.rule import to_me

from .config import Config
from .hoyospider import *
from .utils import *

require("nonebot_plugin_templates")
from nonebot_plugin_templates.template_types import *
from nonebot_plugin_templates.templates_render import menu_render

try:
    scheduler = require("nonebot_plugin_apscheduler").scheduler
except:
    scheduler = None
try:
    import ujson as json
except ModuleNotFoundError:
    import json
from nonebot_plugin_apscheduler import scheduler
import asyncio
import re

__plugin_meta__ = PluginMetadata(
    name="米游社cos",
    description="获取原神coser图片",
    config=Config,
    usage="原神cos,CosPlus,下载cos",
    type="application",
    homepage="https://github.com/Cvandia/nonebot_plugin_genshin_cos",
    supported_adapters={"~onebot.v11"},
    extra={
        "unique_name": "genshin_cos",
        "example": "保存cos:保存cos图片至本地文件",
        "author": "divandia <106718176+Cvandia@users.noreply.github.com>",
        "version": "0.2.0",
    },
)
logo = """<g>
  /$$$$$$                                /$$       /$$                  /$$$$$$                     
 /$$__  $$                              | $$      |__/                 /$$__  $$                    
| $$  \__/  /$$$$$$  /$$$$$$$   /$$$$$$$| $$$$$$$  /$$ /$$$$$$$       | $$  \__/  /$$$$$$   /$$$$$$$
| $$ /$$$$ /$$__  $$| $$__  $$ /$$_____/| $$__  $$| $$| $$__  $$      | $$       /$$__  $$ /$$_____/
| $$|_  $$| $$$$$$$$| $$  \ $$|  $$$$$$ | $$  \ $$| $$| $$  \ $$      | $$      | $$  \ $$|  $$$$$$ 
| $$  \ $$| $$_____/| $$  | $$ \____  $$| $$  | $$| $$| $$  | $$      | $$    $$| $$  | $$ \____  $$
|  $$$$$$/|  $$$$$$$| $$  | $$ /$$$$$$$/| $$  | $$| $$| $$  | $$      |  $$$$$$/|  $$$$$$/ /$$$$$$$/
 \______/  \_______/|__/  |__/|_______/ |__/  |__/|__/|__/  |__/       \______/  \______/ |_______/ 
 </g>"""

logger.opt(colors=True).info(logo)

# 用户cd数据
user_data = {}
CONFIG: Dict[str, Dict[str, str]] = {"原神": {}, "崩坏3": {}, "大别野": {}, "星穹铁道": {}}
DRIVER = get_driver()

# 读取配置文件
config_path = Path("config/genshincos.json")
config_path.parent.mkdir(parents=True, exist_ok=True)
if config_path.exists():
    with open(config_path, "r", encoding="utf8") as f:
        CONFIG = json.load(f)
else:
    with open(config_path, "w", encoding="utf8") as f:
        json.dump(CONFIG, f, ensure_ascii=False, indent=4)

# 事件响应器
help = on_command("原神cos", aliases={"genshincos"})
download_cos = on_command(
    "下载cos",
    aliases={"cos保存", "保存cos"},
    block=False,
    priority=5,
    permission=SUPER_PERMISSION,
)
hot_cos = on_command("热门cos", aliases={"热门coser", "热门cos图"}, block=False, priority=5)
rank_cos = on_regex(r"^(日|月|周)榜cos[r]?[图]?(.+)?", priority=5, block=False, flags=re.I)
latest_cos = on_command("最新cos", aliases={"最新coser", "最新cos图"}, block=False, priority=5)
good_cos = on_command("精品cos", aliases={"精品coser", "精品cos图"}, block=False, priority=5)
turn_aps = on_regex(
    r"^(开启|关闭)每日推送(原神|崩坏3|星穹铁道|大别野)(\s)?(.+)?",
    block=False,
    priority=5,
    flags=re.I,
    permission=SUPER_PERMISSION,
)
show_aps = on_command(
    "查看本群推送", aliases={"查看推送", "查看订阅"}, block=False, priority=5, rule=to_me()
)

Generated_pic = False
Help_Path = Path(__file__).parent / "Help.jpeg"


@help.handle()
async def _(matcher: Matcher, event: MessageEvent, foo: Annotated[str, CommandStart()]):
    global Generated_pic
    command_start = str(foo)
    if not Generated_pic:
        menu = Menu(
            "原神cos",
            des="获取原神cos图片",
            funcs=Funcs(
                Func(f"{command_start}日、周、月榜cos", "获取排行榜cos图。如日榜cos 原神 x3")
                + Func(f"{command_start}热门cos", "获取指定游戏热门cos图，如热门cos 原神 x3	")
                + Func(f"{command_start}最新cos", "获取指定游戏最新cos图，如最新cos 原神 x3	")
                + Func(f"{command_start}精品cos", "获取指定游戏精品cos图，如精品cos 原神 x3	")
                + Func(f"{command_start}查看本群推送", "查看本群的订阅cos目录")
                + Func(
                    f"{command_start}下载cos", "仅超管、群主、管理员可用\n获取指定游戏热门cos图，如热门cos 原神 x3	"
                )
                + Func(
                    f"{command_start}开启每日推送xx (时间)",
                    "仅超管、群主、管理员可用\n如开启每日推送原神 8:30,注意时间的格式",
                )
            ),
        )
        pic_bytes = await menu_render(Menus(menu), 700)
        with open(Help_Path, "wb") as f:
            f.write(pic_bytes)
        Generated_pic = True
    else:
        with open(Help_Path, "rb") as f:
            pic_bytes = f.read()
    await matcher.send(MessageSegment.image(pic_bytes))


@show_aps.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    send_msg = "本群订阅的推送有:\n"
    for game_type, dict in CONFIG.items():
        if game_type == "":
            continue
        for goup_id, time in dict.items():
            if str(event.group_id) == goup_id:
                send_msg += f"{game_type}的每日{time}推送\n"
    await show_aps.finish(send_msg)


@turn_aps.handle()
async def _(event: GroupMessageEvent, args: Tuple[str, ...] = RegexGroup()):
    # 检查是否安装了apscheduler插件，并且是否开启了定时推送
    if scheduler == None:
        await turn_aps.finish("未安装apscheduler插件,无法使用此功能")
    mode = args[0]
    game_type = args[1]
    time = args[3]
    aps_group_id = str(event.group_id)
    MyConfig = CONFIG.copy()
    if mode == "开启":
        for name in MyConfig.keys():
            if name == game_type:
                if aps_group_id in MyConfig[name].keys():
                    await turn_aps.finish("该群已开启,无需重复开启")
                elif not time:
                    await turn_aps.finish("请指定推送时间")
                else:
                    CONFIG[name][aps_group_id] = time
                    try:
                        scheduler.add_job(
                            aps_send,
                            trigger="cron",
                            hour=time.split(":")[0],
                            minute=time.split(":")[1],
                            id=f"{game_type}{aps_group_id}",
                            args=(aps_group_id,),
                        )
                        logger.debug(f"已成功添加{aps_group_id}的{game_type}定时推送")
                    except Exception as e:
                        logger.error(e)
    else:
        for name in MyConfig.keys():
            if name == game_type:
                if aps_group_id in MyConfig[name].keys():
                    CONFIG[name].pop(aps_group_id)
                    try:
                        scheduler.remove_job(f"{game_type}{aps_group_id}")
                    except Exception as e:
                        logger.error(e)
                        continue
                else:
                    await turn_aps.finish("该群已关闭,无需重复关闭")
    with open(config_path, "w", encoding="utf8") as f:
        f.write(json.dumps(CONFIG, ensure_ascii=False, indent=4))
    await turn_aps.finish(f"已成功{mode}{aps_group_id}的{game_type}定时推送")


@hot_cos.handle()
async def _(
        bot: Bot, matcher: Matcher, event: MessageEvent, arg: Message = CommandArg()
):
    if not arg:
        await hot_cos.finish("请指定cos类型")
    args = arg.extract_plain_text().split()
    if args[0] in GENSHIN_NAME:
        send_type = genshin_hot
    elif args[0] in HONKAI3RD_NAME:
        send_type = honkai3rd_hot
    elif args[0] in DBY_NAME:
        send_type = dbycos_hot
    elif args[0] in STAR_RAIL:
        send_type = starrail_hot
    else:
        await hot_cos.finish("暂不支持该类型")
    await send_images(bot, matcher, args, event, send_type)


@rank_cos.handle()
async def _(
        bot: Bot,
        matcher: Matcher,
        event: MessageEvent,
        group: Tuple[str, ...] = RegexGroup(),
):
    if not group[1]:
        await rank_cos.finish("请指定cos类型")
    args = group[1].split()
    if group[0] == "日":
        rank_type = RankType.Daily
    elif group[0] == "周":
        rank_type = RankType.Weekly
    elif group[0] == "月":
        rank_type = RankType.Monthly

    if args[0] in GENSHIN_NAME:
        send_type = Rank(ForumType.GenshinCos, rank_type)
    elif args[0] in HONKAI3RD_NAME:
        send_type = Rank(ForumType.Honkai3rdPic, rank_type)
    elif args[0] in DBY_NAME:
        send_type = Rank(ForumType.DBYCOS, rank_type)
    elif args[0] in STAR_RAIL:
        send_type = Rank(ForumType.StarRailCos, rank_type)
    else:
        await rank_cos.finish("暂不支持该类型")
    await send_images(bot, matcher, args, event, send_type)


@latest_cos.handle()
async def _(
        bot: Bot, matcher: Matcher, event: MessageEvent, arg: Message = CommandArg()
):
    if not arg:
        await latest_cos.finish("请指定cos类型")
    args = arg.extract_plain_text().split()
    if args[0] in GENSHIN_NAME:
        send_type = genshin_latest_comment
    elif args[0] in HONKAI3RD_NAME:
        send_type = honkai3rd_latest_comment
    elif args[0] in DBY_NAME:
        send_type = dbycos_latest_comment
    elif args[0] in STAR_RAIL:
        send_type = starrail_latest_comment
    else:
        await latest_cos.finish("暂不支持该类型")
    await send_images(bot, matcher, args, event, send_type)


@good_cos.handle()
async def _(
        bot: Bot, matcher: Matcher, event: MessageEvent, arg: Message = CommandArg()
):
    if not arg:
        await good_cos.finish("请指定cos类型")
    args = arg.extract_plain_text().split()
    if args[0] in GENSHIN_NAME:
        await good_cos.finish("原神暂不支持精品cos")
    elif args[0] in HONKAI3RD_NAME:
        send_type = honkai3rd_good
    elif args[0] in DBY_NAME:
        send_type = dbycos_good
    elif args[0] in STAR_RAIL:
        await good_cos.finish("星穹铁道暂不支持精品cos")
    else:
        await good_cos.finish("暂不支持该类型")
    await send_images(bot, matcher, args, event, send_type)


@download_cos.got("game_type", prompt="你想下载哪种类型的,有原神和大别野,崩坏3,星穹铁道")
async def got_type(game_type: str = ArgPlainText()):
    if game_type in GENSHIN_NAME:
        hot = genshin_hot
    elif game_type in DBY_NAME:
        hot = dbycos_hot
    elif game_type in HONKAI3RD_NAME:
        hot = honkai3rd_hot
    elif game_type in STAR_RAIL:
        hot = starrail_hot
    image_urls = await hot.async_get_urls()
    if not image_urls:
        await download_cos.finish(f"没有找到{game_type}的cos图片")
    else:
        await download_cos.send(f"正在下载{game_type}的cos图片")
        try:
            await download_from_urls(image_urls, SAVE_PATH / f"{game_type}cos")
            await download_cos.finish(f"已成功保存{len(image_urls)}张{game_type}的cos图片")
        except WriteError as e:
            await download_cos.finish(f"保存部分{game_type}的cos图片失败,原因:{e}")


###########################################################################################


# 定时任务
async def aps_send(aps_goup_id: str):
    logger.debug("正在发送定时推送")
    bot: Bot = get_bot()
    for game_type, dict in CONFIG.items():
        if game_type == "":
            continue
        for saved_group_id, time in dict.items():
            if not (
                    datetime.now().hour == int(time.split(":")[0])
                    and datetime.now().minute == int(time.split(":")[1])
            ):
                continue
            elif saved_group_id != aps_goup_id:
                continue
            try:
                group_id = int(saved_group_id)
                if game_type in GENSHIN_NAME:
                    send_type = genshin_rank_daily
                elif game_type in DBY_NAME:
                    send_type = dby_rank_daily
                elif game_type in HONKAI3RD_NAME:
                    send_type = honkai3rd_rank_daily
                elif game_type in STAR_RAIL:
                    send_type = starrail_rank_daily
                else:
                    continue
                image_list = await send_type.async_get_urls(page_size=5)
                name_list = await send_type.async_get_name(page_size=5)
                rank_text = "\n".join(
                    [f"{i + 1}.{name_list[i]}" for i in range(len(name_list))]
                )
                msg_list = [f"✅米游社{game_type}cos每日榜单✅"]
                msg_list.append(rank_text)
                msg_list.append([MessageSegment.image(img) for img in image_list])
                msg_list = msglist2forward("米游社cos", "2854196306", msg_list)
                await bot.call_api(
                    "send_group_forward_msg", group_id=group_id, messages=msg_list
                )
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(e)


async def send_images(
        bot: Bot,
        matcher: Matcher,
        args: list,
        event: MessageEvent,
        send_type: HoyoBasicSpider,
):
    """
    发送图片

    params:
        bot: 当前bot
        matcher: 事件响应器
        args: 命令参数(0:类型 1:数量)
        event: 消息事件类型
        send_type: 爬虫类型
    """
    global user_data
    out_cd, deletime, user_data = check_cd(event.user_id, user_data)
    if out_cd:
        if len(args) < 2:
            await matcher.send("获取图片中…请稍等")
            try:
                image_list = await send_type.async_get_urls()
                await matcher.send(MessageSegment.image(choice(image_list)))
            except ActionFailed:
                await matcher.finish("账户风控了,发送不了图片", at_sender=True)
        else:
            num = int(re.sub(r"[x|*|X]", "", args[1]))
            num = num if num <= MAX else MAX
            msg_list = [f"✅找到最新的一些{args[0]}图如下:✅"]
            image_list = await send_type.async_get_urls()
            if num > len(image_list):
                await matcher.finish(f"最多只能获取{len(image_list)}张图片", at_sender=True)
            for i in range(num):
                msg_list.append(MessageSegment.image(image_list[i]))
            if IS_FORWARD:
                await send_forward_msg(bot, event, "米游社cos", bot.self_id, msg_list)
            else:
                await send_regular_msg(matcher, msg_list)
    else:
        await matcher.finish(f"cd冷却中,还剩{deletime}秒", at_sender=True)


@DRIVER.on_startup
async def start_aps():
    try:
        if scheduler == None:
            logger.error("未安装apscheduler插件,无法使用此功能")
        with open(config_path, "r", encoding="utf8") as f:
            CONFIG = json.load(f)
        for game_type, dict in CONFIG.items():
            if game_type == "":
                continue
            for aps_group_id, time in dict.items():
                if time == "":
                    continue
                try:
                    scheduler.add_job(
                        aps_send,
                        trigger="cron",
                        hour=time.split(":")[0],
                        minute=time.split(":")[1],
                        id=f"{game_type}{aps_group_id}",
                        args=(aps_group_id,),
                    )
                    logger.debug(f"已成功添加{aps_group_id}的{game_type}定时推送")
                except Exception as e:
                    logger.error(e)
                    continue
    except Exception as e:
        logger.error(e)
