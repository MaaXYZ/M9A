# M9A

基于全新架构的 亿韭韭韭 小助手。图像技术 + 模拟控制，解放双手！  
由 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 强力驱动！

## 功能介绍

目前已有的功能：

- 启动/关闭游戏
- 收取荒原、魔精收取生产物品
- 每日心相（意志解析）
- 刷体力、最优材料关卡、活动关卡导航、吃糖选项
- 领取日常奖励
- 轶事派遣
- 雨中悬想：迷思海（“寻思”每周扫荡）
- 局外演绎：山麓的回音（肉鸽）
- 每周深眠域（使用游戏自带自动战斗）

近期可能会支持的功能：
- 自定义刷体力关卡

## 使用说明

下载地址：<https://github.com/MaaXYZ/M9A/releases>

PS: 可以连接模拟器和手机, 但需要屏幕比例为 16:9

### Windows

- 对于绝大部分用户，请下载 `M9A-win-x86_64-vXXX.zip`
- 若确定自己的电脑是 arm 架构，请下载 `M9A-win-aarch64-vXXX.zip`  
  _请注意！Windows 的电脑几乎全都是 x86_64 的，可能占 99.999%，除非你非常确定自己是 arm，否则别下这个！_
- 解压后运行 `MFAWPF.exe`（图形化界面）或 `MaaPiCli.exe`（命令行）即可

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

## 其他说明

- 提示“应用程序错误”，一般是缺少运行库，请安装一下 [vc_redist](https://aka.ms/vs/17/release/vc_redist.x64.exe)
- 添加 `-d` 参数可跳过交互直接运行任务，如 `./MaaPiCli.exe -d`
- 2.0 版本已支持 mumu 后台保活，会在 run task 时获取 mumu 最前台的 tab
- 反馈问题请附上日志文件 `debug/maa.log`以及问题界面的截图，谢谢！



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

- [MaaFW 开发思路](https://github.com/MaaXYZ/MaaFramework/blob/main/docs/zh_cn/1.1-%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.md#%E5%BC%80%E5%8F%91%E6%80%9D%E8%B7%AF)  
  M9A 目前使用其中第一种方式（纯 Pipeline 低代码），后续可能会迁移到第二种方式（Pipeline + 自定义任务）
- [Pipeline 流水线协议](https://github.com/MaaXYZ/MaaFramework/blob/main/docs/zh_cn/3.1-%E4%BB%BB%E5%8A%A1%E6%B5%81%E6%B0%B4%E7%BA%BF%E5%8D%8F%E8%AE%AE.md)

更多文档请前往 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 主仓库查看

## 鸣谢

本项目由 **[MaaFramework](https://github.com/MaaXYZ/MaaFramework)** 强力驱动！

感谢以下开发者对本项目作出的贡献:

<a href="https://github.com/MaaXYZ/M9A/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=MaaXYZ/M9A&max=1000" />
</a>

## Join us
- M9A 闲聊群 QQ 群：175638678
- M9A 开发群 QQ 群：649344857
- MaaFramework 开发交流 QQ 群: 595990173
