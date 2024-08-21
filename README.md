<div align="center">

# MAA_SnowBreak

基于全新架构的 尘白禁区 小助手。图像技术 + 模拟控制，解放双手！  
由 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 强力驱动！


</div>

## 主要功能

- 启动/关闭游戏
- 收取赠送感知
- 升级枪械
- 领取邮件
- 商店自动购买指定物品[物品列表](docs/物品列表.md)
- 领取体力
- 日常作战和活动作战
- 刷天启碎片
- 领取凭证和任务奖励
- 基地疗愈任务（需要进入疗愈界面）
- 钓鱼(需要进入钓鱼界面）

## 注意事项
- 安卓模拟器必须为mumu模拟器,如果出现部分任务无法完成,请切换1280*720(240DPI)
- 桌面端显示器必须为标准16:9显示器,且游戏必须为无边框窗口

## 图形化界面

### [MFAWPF](https://github.com/SweetSmellFox/MFAWPF)
 由社区大佬编写的基于WPF的GUI,通过内置的MAAframework来直接控制任务流程
 -下载`MSBA-win-x86_64-vXXX-with-GUI.zip`
  
## 视频教程

- 教程: <https://www.bilibili.com/video/BV1v2hFe8Esv/>
- 计划任务教程: <https://www.bilibili.com/video/BV1Nuh2eGEwG/>
  
## 使用说明

下载地址：<https://github.com/overflow65537/MAA_SnowBreak/releases>

### Windows

- 对于绝大部分用户，请下载 `MSBA-win-x86_64-vXXX.zip`
- 若确定自己的电脑是 arm 架构，请下载 `MSBA-win-aarch64-vXXX.zip`
- 解压后以***管理员权限***运行 `MaaPiCli.exe` 即可

### macOS

- 若使用 Intel 处理器，请下载 `MSBA-macos-x86_64-vXXX.zip`
- 若使用 M1, M2 等 arm 处理器，请下载 `MSBA-macos-aarch64-vXXX.zip`
- 使用方式：

  ```bash
  chmod a+x MaaPiCli
  ./MaaPiCli
  ```

### Linux

~~用 Linux 的大佬应该不需要我教~~
## MaaPiCli使用说明
### A
- 启动后会出现:
```
Welcome to use Maa Project Interface CLI!

Version: v0.0.1

### Select ADB ###

        1. Auto detect
        2. Manual input

Please input [1-2]:
```
- 如无必要，请选择1.Auto detect

```
### Select ADB ###

        1. Auto detect
        2. Manual input

Please input [1-2]: 1

Finding device...

## Select Device ##

        1. MuMuPlayer12
                H:/Program Files/Netease/MuMuPlayer-12.0/shell/adb.exe
                127.0.0.1:16672

Please input [1-1]: 1
```
- 选择 1 后会像上面这样，列出若干个模拟器实例，之后选择你需要进行操控的即可。
- 如果没有出现选项，请检查模拟器是否正常启动。以及管理员权限启动MaaPiCli。
### B
- 选择完模拟器后就会进入到选择资源界面
```
### Select resource ###

        1. 官服
        2. B 服

Please input [1-2]:
```
- 请按照自己的服务器类型选择
### C
- 在初次启动后，会让你输入启动的任务：
```
### Add task ###

        1. 启动
        2. 赠送感知
        3. 邮件
        4. 商店
        5. 领取体力
        6. 升级枪械
        7. 活动
        8. 常规战斗
        9. 刷天启碎片
        10. 任务
        11. 活动任务
        12. 凭证
        13. 关闭游戏

Please input [1-13]:
```
- 选择你要执行的任务即可。

### D

- 之后会反复出现：
```
Tasks:

<这里会列出你已经增加，等待执行的任务>

### Select action ###

        1. Switch controller
        2. Switch resource
        3. Add task
        4. Move task
        5. Delete task
        6. Run tasks
        7. Exit
```
- 其中分别代表：
1. 调整控制器（也就是adb地址等）
2. 调整资源（切换官服或者b服）
3. 新增任务，像**C**中那样
4. 移动任务
5. 删除任务
6. 开始执行任务，在这之后就会自动开始操控。
7. 退出程序

## 其他说明

- 添加 `-d` 参数可跳过交互直接运行任务，如 `./MaaPiCli.exe -d`，配合Windows计划任务可以实现自动开启任务
- 反馈问题请附上日志文件 `debug/maa.log`，谢谢！

## How to build

**如果你要编译源码才看这节，否则直接 [下载](https://github.com/overflow65537/MAA_SnowBreak/releases) 即可**

0. 完整克隆本项目及子项目

    ```bash
    git clone --recursive https://github.com/overflow65537/MAA_SnowBreak.git
    ```

1. 下载 MaaFramework 的 [Release 包](https://github.com/MaaXYZ/MaaFramework/releases)，解压到 `deps` 文件夹中
2. 安装

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

本项目由 **[MaaFramework](https://github.com/MaaXYZ/MaaFramework)** 强力驱动！

