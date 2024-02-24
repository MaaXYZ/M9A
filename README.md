# M9A

基于全新架构的 亿韭韭韭 小助手。图像技术 + 模拟控制，解放双手！  
由 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 强力驱动！

## 功能介绍

目前已有的功能：

- 启动/关闭游戏
- 收取荒原
- 每日心相（意志解析）
- 刷体力、常用主线/活动关卡导航、吃糖选项
- 山麓的回音（肉鸽）
- 领取日常奖励

近期可能会支持的功能：

- 每周深眠域（使用游戏自带自动战斗）
- 重新整理最优刷体力关卡
- 自定义刷体力关卡

## 下载说明

下载地址：<https://github.com/MaaXYZ/M9A/releases>

### Windows

- 对于绝大部分用户，请下载 `M9A-win-x86_64-vXXX.zip`
- 若确定自己的电脑是 arm 架构，请下载 `M9A-win-aarch64-vXXX.zip`
- 解压后运行 `MaaPiCli.exe` 即可

### macOS

- 若使用 Intel 处理器，请下载 `M9A-macos-x86_64-vXXX.zip`
- 若使用 M1, M2 等 arm 处理器，请下载 `M9A-macos-aarch64-vXXX.zip`
- 使用方式：

  ```bash
  chmod a+x MaaPiCli
  ./MaaPiCli
  ```

### Linux

~~用 Linux 的大佬应该不需要我教~~

## 图形化界面

目前暂无正式版 GUI，但有以下由社区大佬们贡献的 GUI 项目，欢迎使用！

- [MAA1999WPF](https://github.com/MLAcookie/MAA1999WPF) 拿WPF框架写的一个MAA199的UI

## How to build

**如果你要编译源码才看这节，否则直接 [下载](https://github.com/MaaXYZ/M9A/releases) 即可**

0. 完整克隆本项目及子项目

    ```bash
    git clone --recursive https://github.com/MaaXYZ/M9A.git
    ```

1. 下载 MaaFramework 的 [Release 包](https://github.com/MaaXYZ/MaaFramework/releases)，解压到 `deps` 文件夹中
2. 安装

    ```python
    python ./install.py
    ```

生成的二进制及相关资源文件在 `install` 目录下

## 开发相关

- [MaaFramework 快速开始](https://github.com/MaaXYZ/MaaFramework/blob/main/docs/zh_cn/1.1-%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.md)

## Join us

- 1999 开发交流 QQ 群：649344857
- MaaFramework 开发交流 QQ 群: 595990173
