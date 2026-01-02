<!-- markdownlint-disable MD033 MD041 -->

<p align="center">
  <img alt="LOGO" src="logo.png" width="256" height="256" />
</p>

<div align="center">

# MAA_SnowBreak

基于全新架构的 尘白禁区 小助手。图像技术 + 模拟控制，解放双手！
由 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 强力驱动！

</div>

<p align="center">
  <img alt="license" src="https://img.shields.io/github/license/overflow65537/MAA_SnowBreak">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">
  <img alt="platform" src="https://img.shields.io/badge/platform-Windows-blueviolet">
  <img alt="commit" src="https://img.shields.io/github/commit-activity/m/overflow65537/MAA_SnowBreak">
  <img alt="mirrorchyan_rid" src="https://img.shields.io/badge/mirrorchyan_rid-MAA__SnowBreak-orange">
</p>

## 免责条款

- 本资源按“现状”提供，不附带任何形式的明示或暗示担保。使用者需自行承担所有风险。
- 作者不对因使用本资源而导致的任何直接、间接或结果性损失承担责任。
- 本资源为独立组件，其MIT许可证不传染，也不受与之集成的其他软件许可证的影响。
- 基于本资源进行的任何商业行为均与原作者无关，使用者不得暗示任何官方关联或认可。

## 主要功能

- 启动/关闭游戏
- 收取赠送感知
- 升级枪械
- 领取邮件
- 商店自动购买指定物品[物品列表](docs/物品列表.md)
- 领取体力
- 精神拟境自动评测
- 日常作战和活动作战
- 刷天启碎片
- 领取凭证和任务奖励
- 自动信源研析
- 基地疗愈
- 钓鱼
- 心动水弹
- 猜心对局
- 异星守护
- 悖论迷宫（验证战场）
- 蜃梦笔谈
- 捞金派对

## 注意事项

- 安卓端：~~模拟器必须为mumu模拟器~~任意模拟器皆可（赞美lhm）,如果出现部分任务无法完成,请切换1280*720(240DPI)
- 桌面端：需要使用管理员权限启动
- PlayCover端：支持,但没有测试,如果有问题请反馈
- 打开后无法运行首先尝试安装运行库 [https://learn.microsoft.com/zh-cn/cpp/windows/latest-supported-vc-redist?view=msvc-170](https://learn.microsoft.com/zh-cn/cpp/windows/latest-supported-vc-redist?view=msvc-170)
- 反馈 QQ 群：980583911

## 使用说明

下载地址：[https://github.com/overflow65537/MAA_SnowBreak/releases](https://github.com/overflow65537/MAA_SnowBreak/releases)

### Windows

- 对于绝大部分用户，请下载 `MSBA-win-x86_64-vXXX.zip`
- 若确定自己的电脑是 arm 架构，请下载 `MSBA-win-aarch64-vXXX.zip`
- 解压后运行 `MaaPiCli.exe`（命令行）或者`MFW.exe`（图形化界面） 即可

### macOS

- 若您的 Mac 采用 Intel 处理器，请下载 `MSBA-macos-x86_64-vXXX.tar.gz`
- 若您的 Mac 采用 M1、M2 等 ARM 处理器，请下载 `MSBA-macos-aarch64-vXXX.tar.gz`
- 使用方法如下：
  1. 打开终端，解压下载的压缩包，您有以下三种解压方式可供选择：

      **选项 1：解压到系统目录（需管理员权限）**
      此方式将把程序解压到系统目录，需要输入管理员密码获取权限。

      ```zsh
      sudo mkdir -p /usr/local/bin/MSBA
      sudo tar -xzf <下载的MSBA压缩包路径> -C /usr/local/bin/MSBA
      ```

      **选项 2：解压到用户目录（推荐）**
      该方式无需管理员权限，操作简便且便于管理个人文件。

      ```zsh
      mkdir -p ~/MSBA
      tar -xzf <下载的MSBA压缩包路径> -C ~/MSBA
      ```

      **选项 3：直接解压到下载目录（不推荐）**
      这种方式操作快捷，但可能会导致 `Downloads` 文件夹文件杂乱。您只需双击下载的 MSBA 压缩包，即可在同级目录自动解压。

  2. 进入解压目录并运行程序：
      - 根据上一步选择的解压方式操作：
          - 若选择选项 1 ，在终端中执行以下命令打开程序目录：

          ```zsh
          open /usr/local/bin/MSBA
          ```

          - 若选择选项 2，在终端中执行以下命令打开程序目录：

          ```zsh
          open ~/MSBA
          ```

          - 若选择选项 3，直接双击解压后的文件夹进入。
      - 找到 `MFW` 程序并双击运行。

  ⚠️Gatekeeper 安全提示处理：
  在 macOS 10.15 (Catalina) 及更高版本中，Gatekeeper 可能会阻止运行未签名的应用程序。若遇到“无法打开，因为无法验证开发者”,或者“已损坏”等错误，请使用以下命令移除隔离属性：

  ```zsh
  sudo xattr -rd com.apple.quarantine /usr/local/bin/MSBA/*
  # 若选择选项 2，解压到用户目录，使用以下命令：xattr -rd com.apple.quarantine ~/MSBA/*
  # 若选择选项 3，直接解压到下载目录，使用以下命令：xattr -rd com.apple.quarantine <下载目录>/MSBA/*


### Linux

~~用 Linux 的大佬应该不需要我教~~

## 视频教程

- 教程: [https://www.bilibili.com/video/BV1v2hFe8Esv/](https://www.bilibili.com/video/BV1v2hFe8Esv/)
- 计划任务教程: [https://www.bilibili.com/video/BV1Nuh2eGEwG/](https://www.bilibili.com/video/BV1Nuh2eGEwG/)

## How to build

**如果你要编译源码才看这节，否则直接 [下载](https://github.com/overflow65537/MAA_SnowBreak/releases) 即可**

0. 完整克隆本项目及子项目

   ```bash
   git clone --recursive https://github.com/overflow65537/MAA_SnowBreak.git
   ```

1. 安装

   ```python
   python ./install.py
   ```

生成的二进制及相关资源文件在 `install` 目录下

## 开发相关

- [MaaFramework 快速开始](https://github.com/MaaAssistantArknights/MaaFramework/blob/main/docs/zh_cn/1.1-%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.md)

## Join us

- 交流反馈 QQ 群：980583911
- MaaFramework 开发交流 QQ 群: 595990173

## 鸣谢

### 开源库

- [MaaFramework](https://github.com/MaaXYZ/MaaFramework)
  基于图像识别的自动化黑盒测试框架 | An automation black-box testing framework based on image recognition
- ~~[MFAWPF](https://github.com/SweetSmellFox/MFAWPF)~~
  ~~本项目是一个基于WPF框架开发的用户界面，旨在提供类似于MaaPiCli的功能~~
- [MFW-CFA](https://github.com/overflow65537/MFW-PyQt6)
  一个基于PySide6的MAAFramework图形化操作界面
- [SnowbreakAutoAssistant](https://github.com/LaoZhuJackson/SnowbreakAutoAssistant)
  PC自动玩尘白，自动化代理，尘白禁区助手，自动钓鱼，信源解析，水弹，异星守护，迷宫
- [cbjq](https://github.com/CmdBlockZQG/cbjq)
  尘白禁区 信源研析小工具

### 开发者

感谢以下开发者对 MAA_SnowBreak 作出的贡献：

<a href="https://github.com/overflow65537/MAA_SnowBreak/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=overflow65537/MAA_SnowBreak&max=1000" alt="Contributors to MAA_SnowBreak"/>
</a>
