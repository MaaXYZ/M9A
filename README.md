# MAA1999

占坑.jpg

## 画大饼

- 自动收菜  
  最基本的了，没啥好说的
- 关卡掉落识别  
  有佬在搓类似企鹅的东西了，[圣洛夫数据部](https://github.com/St-Pavlov-Data-Department)，欢迎加入！
- 自动战斗  
  这游戏的自动战斗有点小难度，但又没粥那么难。我觉得完全可以做到打的比大多数玩家水平高，纯粹的无感情的概率 + 数值机器

## 目前进度

- [x] [框架](https://github.com/MaaAssistantArknights/MaaFramework) 基本完成
- [x] 收菜功能写完了，启动游戏 + 收荒原 + 每日心相 + 日常奖励

## How to build

**如果你要编译源码才看这里，否则直接 [下载](https://github.com/MaaAssistantArknights/MAA1999/releases) 就行了**

_只是一个临时的编译方法，因为 MAA 新架构还缺少一块重要拼图 [MaaCommon](https://github.com/MaaAssistantArknights/MaaCommon)（欢迎大佬们来带带），所以先简单糊一下_

1. 更新子模块 `git submodule update --init --recursive`
2. 下载 MaaFramework 的 Release 包，解压到 `source\cli\x64\Release`
3. 使用 Visual Studio 编译 `source\cli\MAA1999_CLI.sln`

## Join us

开发 QQ 群：649344857
