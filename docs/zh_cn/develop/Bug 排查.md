# Bug 排查

修 bug 也是开发中重要的一环，如何快速准确地定位、分析、解决 bug 是有技巧的。本文将介绍一些常见的 bug 排查方法。

> [!NOTE]
>
> 以下内容仅供参考，注意时效性。

## 前置准备

与 bug 发现者沟通，尽可能的获取 bug 相关的信息，如：

- 资源版本
- 系统版本
- 问题的细节（发生的时间、场景等）
- 配置文件、日志、截图等

## 定位问题

### 确认资源版本以及运行方式

对于 M9A 来说，有两种运行方式：1. MaaPiCli 2. MFAWPF

根据观察，MaaPiCli运行时有行log为

```plaintext
[2024-11-28 19:46:32.571][INF][Px14600][Tx16498][Parser.cpp][L56][MaaNS::ProjectInterfaceNS::Parser::parse_interface] Interface Version: [data.version=v2.4.11]
```

既能看出资源版本，又能看出是以 MaaPiCli 方式运行。

```plaintext
[2024-11-30 01:46:56.490][INF][Px20060][Tx33876][Parser.cpp][L56][MaaNS::ProjectInterfaceNS::Parser::parse_interface] Interface Version: [data.version=] 
```

当 `version` 为空时，MaaPiCli log 为以上样式。

确认资源版本可以了解是否为已修复bug版本，确认运行方式则是因为不同运行方式，config文件不同，同时可能生成的bug也不同。

### 确定问题 log 范围

- 根据问题描述发生的时间缩小范围
- 根据问题发生的任务缩小范围
- 根据[ERR]确定错误相关原因
- 根据bug相关的[ERR]处反向查找 `Task Hit` ，以确定出错任务

## 分析问题

在这里我将问题大致分为三类：资源加载问题、连接问题以及 pipeline 问题（timeout）。

### 资源加载问题

资源改名时覆盖安装导致的资源加载失败：

```log
[2024-11-17 22:29:04.185][ERR][Px10564][Tx9380][PipelineResMgr.cpp][L211][MaaNS::ResourceNS::PipelineResMgr::parse_config] key already exists [key=OutsideDeduction] 
```

### 连接问题

模拟器连接失败：

```log
[2024-11-24 23:44:05.539][ERR][Px26056][Tx55883][ControlUnitMgr.cpp][L55][MaaNS::CtrlUnitNs::ControlUnitMgr::connect] failed to connect [adb_path_=D:/MuMu Player 12/shell/adb.exe] [adb_serial_=127.0.0.1:16384]
```

### pipeline 问题

一般来说，是pipeline逻辑有漏洞导致的，需要进一步分析。

常用的解决方法有：

- 增加 `flag` 任务
- 增加 `pre/post_wait_freezes` （注意默认 `target` 是否是你想要的）
- 更改实现逻辑（如更换识别方式以及动作逻辑）

## 解决问题

前两种参考[常见问题](../manual/常见问题.md)解决，pipeline 问题需要进一步分析。

## 验证修复

修复后发布测试版，经测试无误后解决问题。
