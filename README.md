![056131D4](https://github.com/Cvandia/nonebot_plugin_genshin_cos/assets/106718176/da116fce-d24f-4f89-8f6c-1f2509fd56be)
<div align="center">

<a href="https://v2.nonebot.dev/store"><img src="https://ghproxy.com/https://github.com/Cvandia/nonebot_plugin_genshin_cos/blob/main/res/ico.png" width="180" height="180" alt="NoneBotPluginLogo"></a>

</div>

<div align="center">

# nonebot-plugin-fakemsg

_⭐基于Nonebot2的一款获取米游社cos的插件⭐_


</div>

<div align="center">
<a href="https://www.python.org/downloads/release/python-390/"><img src="https://img.shields.io/badge/python-3.8+-blue"></a>  <a href=""><img src="https://img.shields.io/badge/QQ-1141538825-yellow"></a> <a href="https://github.com/Cvandia/nonebot-plugin-fakemsg/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue"></a> <a href="https://v2.nonebot.dev/"><img src="https://img.shields.io/badge/nonebot2-2.0.0+-red"></a>
</div>


## ⭐ 介绍

> 什么？你也想让你朋友出糗？！来试试伪造他的消息吧



<div align="center">

#### 有啥关于该插件的新想法的，可以提issue或者pr (>A<)

</div>

## 💿 安装

<details>
<summary>安装</summary>

pip 安装

```
pip install nonebot-plugin-fakemsg
```
- 在nonebot的pyproject.toml中的plugins = ["xxx"]添加此插件

nb-cli安装

```
nb plugin install nonebot-plugin-fakemsg --upgrade
```

git clone安装(不推荐)

- 运行
`git clone https://github.com/Cvandia/nonebot-plugin-fakemsg`
- 在运行处
把文件夹`nonebot_plugin_fakemsg`复制到bot根目录下的`src/plugins`(或者你创建bot时的其他名称`xxx/plugins`)

 
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
|fake_split|str|'\|'|不同人伪造消息的分隔符|

## ⭐ 使用
<details>
<summary>使用效果图如下</summary>

![效果图1]()

</details>


**注意**
> 指令触发方式是正则匹配的，不需要加指令前缀

## 🌙 未来
 - [x] 暂无其他规划

--- 喜欢记得点个star⭐---

## 💝 特别鸣谢

- [x] [Nonebot](https://github.com/nonebot/nonebot2): 本项目的基础，非常好用的聊天机器人框架。
