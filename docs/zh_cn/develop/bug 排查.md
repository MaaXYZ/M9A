# bug 排查

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

### 确认运行方式

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

### 确定问题 log 范围

- 根据问题描述发生的时间缩小范围
- 根据问题发生的任务缩小范围
- 根据[ERR]确定错误范围
- 根据 `Task timeout` 确认范围
- 根据 `Task Hit` 确定 pipeline 流程

## 分析问题

在这里我将问题大致分为三类：资源加载问题、连接问题以及 pipeline 问题（timeout）。

## 解决问题

前两种参考[常见问题](../manual/常见问题.md)解决，pipeline 问题需要进一步分析。

## 验证修复

修复后发布测试版，经测试无误后解决问题。
