![056131D4](https://github.com/Cvandia/nonebot_plugin_genshin_cos/assets/106718176/da116fce-d24f-4f89-8f6c-1f2509fd56be)
<div align="center">

<a href="https://v2.nonebot.dev/store"><img src="https://ghproxy.com/https://github.com/Cvandia/nonebot_plugin_genshin_cos/blob/main/res/ico.png" width="180" height="180" alt="NoneBotPluginLogo"></a>

</div>

<div align="center">

# nonebot-plugin-genshin-cos

_⭐基于Nonebot2的一款获取米游社cos的插件⭐_


</div>

<div align="center">
<a href="https://www.python.org/downloads/release/python-390/"><img src="https://img.shields.io/badge/python-3.8+-blue"></a>  <a href=""><img src="https://img.shields.io/badge/QQ-1141538825-yellow"></a> <a href="https://github.com/Cvandia/nonebot_plugin_genshin_cos/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue"></a> <a href="https://v2.nonebot.dev/"><img src="https://img.shields.io/badge/Nonebot2-rc1+-red"></a>
</div>


## ⭐ 介绍

受到[教程](https://juejin.cn/post/6990320268010848286)的启发，所以写了这个插件，更多功能后续更新~~我很懒，学业重~~



<div align="center">

### 或者你有啥关于该插件的新想法的，可以提issue或者pr (>A<)
### 不仅有原神，现在支持崩坏3、星穹铁道、大别野的cos图！

</div>

## 💿 安装

<details>
<summary>安装</summary>

pip 安装

```
pip install nonebot-plugin-genshin-cos
```
- 在nonebot的pyproject.toml中的plugins = ["xxx"]添加此插件

nb-cli安装

```
nb plugin install nonebot-plugin-genshin-cos --upgrade
```

git clone安装(不推荐)

- 运行
```git clone https://github.com/Cvandia/nonebot_plugin_genshin_cos```
- 在运行处
把文件夹`nonebot-plugin-genshen-cos`复制到bot根目录下的`src/plugins`(或者你创建bot时的其他名称`xxx/plugins`)

 
 </details>
 
 <details>
 <summary>注意</summary>
 
 推荐镜像站下载
  
 清华源```https://pypi.tuna.tsinghua.edu.cn/simple```
 
 阿里源```https://mirrors.aliyun.com/pypi/simple/```

</details>


## ⚙️ 配置
### 在env.中添加以下配置

| 配置 | 类型 | 默认值 | 说明 |
|:-----:|:----:|:----:|:---:|
|cos_max|int|5|最大返回cos图片数量|
|cos_path|str|无|不配置则默认下载到bot根目录的`"data/genshin_cos"`,支持绝对路劲如`"C:/Users/image"`和相对bot根目录路劲如`"coser/image"`
|cos_cd|int|30|用户触发cd|
|cos_forward_msg|bool|True|默认是否合并转发|
|cos_delay|float|0.5|当上面的配置项为`False`时，发送图片的每张延迟s|

> 注意：绝对路劲中用`/`，用`\`可能会被转义

## ⭐ 使用

### 指令：
| 指令 | 需要@ | 范围 | 说明 |权限|
|:-----:|:----:|:----:|:----:|:----:|
|下载cos|否|群聊、私聊|下载热门cos图|超管、群主、管理员|
|热门cos|否|同上|获取指定游戏热门cos图，如`热门cos 原神 x3`|全部|
|日、周、月榜cos|否|同上|获取排行榜cos图。如`日榜cos 原神 x3`|全部|
|最新cos|否|同上|和上面差不多，不写了，哼哼|全部|
|精品cos|否|同上|上上面一样的道理！|全部|
|开启每日推送xx (时间)|否|仅群聊|如`开启每日推送原神 8:30`,注意时间的格式|超管、群主、管理员|
|查看本群推送|是|群聊|查看本群的订阅cos目录|全部|

**注意**

指令触发方式是正则匹配的，不需要加指令前缀

## 🌙 未来
 - [x] 缓慢更新，最近学业繁忙哦~
 - [x] 随机发送cos图片
 - [x] 保存cos图
 - [x] 内置cd和用户触发上限
 - [x] 合并转发发送多张cos图

~~playwright获取cos图~~
~~选择发送图库方式：离线 (迅速) or 在线（缓慢、目前是的）~~

 - [x] 支持米游社其他社区cos获取
 - [x] 支持每日推送热榜的cos图

--- 喜欢记得点个star⭐---

## ❗免责声明

图片版权归米游社原神cos社区所属，请尊重
coser的创作权



## 💝 特别鸣谢

- [x] [Nonebot](https://github.com/nonebot/nonebot2): 本项目的基础，非常好用的聊天机器人框架。
- [x] [@qxdn](https://github.com/qxdn):感谢qxdn的[博客文章](https://qianxu.run/2021/11/12/mihoyo-bbs-crawler/),有兴趣大家也去看看咯
