<style>
  .round-image-container {
    position: relative;
    width: 180px;
    height: 180px;
    display: inline-block;
    overflow: hidden;
  }

  .round-image {
    border-radius: 50%;
    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.2);
    border: 4px solid #ffffff;
    transition: transform 0.3s ease-in-out;
    transform: translateX(0);
  }

  .round-image:hover {
    animation: roll-left 1s forwards;
  }

  .logo-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: transparent;
    padding: 10px;
    white-space: nowrap;
    font-size: 20px;
    opacity: 0;
    transition: opacity 0.5s;
  }

  .round-image-container:hover .logo-text {
    opacity: 1;
  }

  @keyframes roll-left {
    from {
      transform: translateX(0);
    }
    to {
      transform: translateX(-200px);
    }
  }
</style>

<script>
  const roundImage = document.querySelector('.round-image');

  roundImage.addEventListener('mouseenter', () => {
    roundImage.style.animationPlayState = 'running';
  });

  roundImage.addEventListener('mouseleave', () => {
    roundImage.style.animationPlayState = 'paused';
  });
</script>

<div align="center">
  <div class="round-image-container">
    <a href="https://onebot.adapters.nonebot.dev">
      <img src="./res/logo.png" width="180" height="180" alt="OnebotLogo" class="round-image">
      <span class="logo-text">什么都没有</span>
    </a>
  </div>
</div>


<div align="center">

# nonebot-plugin-fakemsg

_⭐基于`Nonebot2`的`onebot 11`的合并转发伪造消息插件⭐_


<style>
  .badge {
    display: inline-block;
    transition: transform 0.3s ease-in-out;
  }
  
  .badge:hover {
    transform: scale(1.1);
  }
</style>

<a href="https://www.python.org/downloads/release/python-390/" class="badge">
<img src="https://img.shields.io/badge/python-3.8+-blue">
</a>
<a href="" class="badge">
<img src="https://img.shields.io/badge/QQ-1141538825-yellow">
</a>
<a href="https://github.com/Cvandia/nonebot-plugin-fakemsg/blob/main/LICENSE" class="badge">
<img src="https://img.shields.io/badge/license-MIT-blue">
</a>
<a href="https://v2.nonebot.dev/" class="badge">
<img src="https://img.shields.io/badge/nonebot2-2.0.0+-red">
</a>
<a href="https://onebot.adapters.nonebot.dev" class="badge">
<img src="https://img.shields.io/badge/Onebot%2011-2.2.4+-green">
</a>
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
nb plugin install nonebot-plugin-fakemsg -U
```

git clone安装(不推荐)

- 运行
`git clone https://github.com/Cvandia/nonebot-plugin-fakemsg`
- 在运行处
把文件夹`nonebot-plugin-fakemsg`复制到bot根目录下的`src/plugins`(或者你创建bot时的其他名称`xxx/plugins`)

 
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
