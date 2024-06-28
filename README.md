<div align="center">

# MAA_SnowBreak

基于全新架构的 尘白禁区 小助手。图像技术 + 模拟控制，解放双手！  
由 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 强力驱动！


</div>

## 主要功能

- 启动/关闭游戏
- 领取邮件
- 商店自动购买芳烃塑料
- 领取体力
- 日常作战和活动作战
- 刷天启碎片
- 领取凭证和任务奖励

## 使用说明

下载地址：<https://github.com/overflow65537/MAA_SnowBreak/releases>
### Windows

- 对于绝大部分用户，请下载 `MAA_SnowBreak-win-x86_64-vXXX.zip`
- 若确定自己的电脑是 arm 架构，请下载 `MAA_SnowBreak-win-aarch64-vXXX.zip`
- 解压后运行 `MaaPiCli.exe` 即可

### macOS

- 若使用 Intel 处理器，请下载 `MAA_SnowBreak-macos-x86_64-vXXX.zip`
- 若使用 M1, M2 等 arm 处理器，请下载 `MAA_SnowBreak-macos-aarch64-vXXX.zip`
- 使用方式：

  ```bash
  chmod a+x MaaPiCli
  ./MaaPiCli
  ```

### Linux

~~用 Linux 的大佬应该不需要我教~~
## How to build

**如果你要编译源码才看这节，否则直接 [下载]<https://github.com/overflow65537/MAA_SnowBreak/releases> 即可**

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
## 鸣谢

本项目由 **[MaaFramework](https://github.com/MaaXYZ/MaaFramework)** 强力驱动！

