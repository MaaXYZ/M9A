# 新手上路

## 前置准备

### 1. 确认版本系统

M9A 在 Windows 下仅支持 10 和 11，旧版 Windows 请参阅[常见问题](https://maa.plus/docs/zh-cn/manual/faq.html#%E7%B3%BB%E7%BB%9F%E9%97%AE%E9%A2%98)中的系统问题部分。

### 2. 安装运行库

M9A 需要 VCRedist x64，请右键开始按钮打开终端，在终端内粘贴以下命令回车以进行安装。

```sh
winget install Microsoft.VCRedist.2015+.x64
```

或者点击 [vc_redist.x64](https://aka.ms/vs/17/release/vc_redist.x64.exe) 下载安装。

### 3. 下载正确的版本

下载地址：[https://github.com/MaaXYZ/M9A/releases](https://github.com/MaaXYZ/M9A/releases)

#### Windows

* 对于**绝大部分**用户，请下载 `M9A-win-x86_64-vXXX.zip`
* 若确定自己的电脑是 arm 架构，请下载 `M9A-win-aarch64-vXXX.zip`
  > 请注意！Windows 的电脑几乎全都是 x86\_64 的，可能占 99.999%，除非你非常确定自己是 arm，否则别下这个！
  >
* 解压后运行 `MaaPiCli.exe`（命令行）或 `MFAWPF.exe`（图形化界面）即可

#### macOS

* 若使用 Intel 处理器，请下载 `M9A-macos-x86_64-vXXX.zip`
* 若使用 M1, M2 等 arm 处理器，请下载 `M9A-macos-aarch64-vXXX.zip`
* 使用方式：
  ```shell
  chmod a+x MaaPiCli
  ./MaaPiCli
  ```

#### Linux

待补充

### 4. 正确解压

确认解压完整，并确保将 MAA 解压到一个独立的文件夹中。请勿将 MAA 解压到如 `C:\`、`C:\Program Files\` 等需要 UAC 权限的路径。

> 不要在压缩软件直接打开程序！

### 5. 确认模拟器支持

查阅[模拟器和设备支持](https://maa.plus/docs/zh-cn/manual/device/)，确认正在使用的模拟器支持情况。

### 6. 正确设置模拟器分辨率

模拟器分辨率应为 `16:9` 比例，最低为 `1280x720`

## 初始配置

0. 若需要使用自动检测，则运行**一个**模拟器，并确保没有其他安卓设备连接电脑。
1. 跟随设置指引进行配置，M9A 会自动检测正在运行的模拟器。
2. 添加任务
3. 运行任务

## 进阶配置

[连接设置](#连接设置)

# 部分功能介绍

## 每日心相（意志解析）

完成每日免费的两次意志解析刷取。

> 注：
>
> 1. 仅在有剩余免费次数时会运行
> 2. 运行时固定刷取两次
> 3. 运行时固定刷取意志解析Ⅶ，未解锁时会报错

## 自动深眠

深眠域开启后，尝试自动推图和领取奖励。

> 注：
>
> 1. 编队选项中编队编号为作战前编队由上自下排序
> 2. 上半编队、下半编队分别为深眠上下半作战的队伍
> 3. 由于深眠的特点，请不要选择上下半为同一编队

## 轶事派遣

每日刷取完体力后，尝试完成轶事派遣任务。

> 注：
>
> 请在当期角色故事阅读并领取奖励后使用本任务

## 雨中悬想：迷思海

完成透光层50M后可运行，以完成 `寻思` 扫荡。

## 局外演绎：黄昏的音序

最有用的肉鸽刷取信用功能。

> 注：
>
> 1. 勿挂资料片（挂了也要给你卸了）
> 2. 由于本功能实现较为复杂，容易出现奇奇怪怪的问题。如果有条件请开启模拟器的录屏，发现问题时尽量保留足够的证据（录像、发生时间、截图以及debug目录下maa.log），以便快速定位问题并得到解决

# 连接设置

参考[连接设置 | MaaAssistantArknights](https://maa.plus/docs/zh-cn/manual/connection.html)

# 常见问题

## 软件无法运行/闪退/报错

### 下载/安装问题

- 完整 M9A 软件压缩包命名格式为 "M9A-`平台`-`架构`-`版本`.zip"，其余均为无法单独使用的“零部件”，请仔细阅读。
  在大部分情况下，您需要使用 x64 架构的 M9A，即您需要下载 `MAA-win-x86_64-vXXX.zip`，而非`MAA-win-aarch64-vXXX.zip`。
- 若在某次更新后无法使用，可能是您覆盖安装造成的, 请尝试重新(下载)解压完整包后新文件夹。

### 运行库问题

特征：

1. 使用 MFAWPF 时，出现

```
MFA 遇到了问题
“对类型“MFAWPF.Views.MainWindow”的构造函数执行符合指定的绑定约束的调用时引发了异常。”，行号为“14”，行位置为“24”。
Unable to load DLL 'MaaToolkit' or one of its dependencies: 动态链接库(DLL)初始化例程失败。 (0x8007045A)
详细信息
System.Windows.Markup.XamlParseException: “对类型“MFAWPF.Views.MainWindow”的构造函数执行符合指定的绑定约束的调用时引发了异常。”，行号为“14”，行位置为“24”。
---> System.DllNotFoundException: Unable to load DLL 'MaaToolkit' or one of its dependencies: 动态链接库(DLL)初始化例程失败。 (0x8007045A)
```

2. 在使用MaaPiCli时，出现 `应用程序错误：应用程序无法正常启动`

以上一般便是运行库问题，需要[更新运行库](#2-安装运行库)

### 资源加载失败

删除整个文件夹，重新下载安装 M9A 。

## 连接错误

### 确认 ADB 及连接地址正确

参阅 [连接设置](#连接设置)

### 关闭现有 ADB 进程

关闭 M9A 后查找 `任务管理器` - `详细信息` 中有无名称包含 `adb` 的进程，如有，结束它后重试连接。

### 正确使用多个 ADB

当 ADB 版本不同时，新启动的进程会关闭旧的进程。因此在需要同时运行多个 ADB，如 Android Studio、Alas、手机助手时，请确认它们的版本相同。

### 避免游戏加速器

部分加速器在启动加速和停止加速之后，都需要重启 MAA、ADB 和模拟器再连接。

同时使用 UU 加速器 和 MuMu 12 可以参考[官方文档](https://mumu.163.com/help/20240321/35047_1144608.html)。

### 重启电脑

重启能解决 97% 的问题。（确信

### 换模拟器

请参阅 [模拟器和设备支持](https://maa.plus/docs/zh-cn/manual/device/)。

### 文件下载速度慢

求助群友/到网上查询相关办法。
