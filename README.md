# MAA1999

基于全新架构的 亿韭韭韭 小助手。图像技术 + 模拟控制，解放双手！  
由 [MaaFramework](https://github.com/MaaAssistantArknights/MaaFramework) 强力驱动！

## 画大饼

- [x] 自动收菜  
  最基本的了，没啥好说的。目前已支持 签到 + 收荒原 + 每日心相 + 领邮件和日常。
- [ ] 关卡掉落识别  
  有佬在搓类似企鹅的站点了：[圣洛夫数据部](https://github.com/St-Pavlov-Data-Department)，欢迎加入！
- [ ] 仓库识别 + 材料需求计算 + 关卡导航  
  粥 MAA 没完成的事情，就由我 韭 MAA 来完成（bushi
- [ ] 自动战斗  
  韭的战斗有点小难度，但又没粥那么难。我觉得完全可以做到打的比大多数玩家水平高，纯粹的无感情的概率 + 数值机器。

## How to build

**如果你要编译源码才看这节，否则直接 [下载](https://github.com/MaaAssistantArknights/MAA1999/releases) 即可**

_只是一个临时的编译方法，因为新架构中的 [MaaCommon](https://github.com/MaaAssistantArknights/MaaCommon) 还没完成，所以先简单糊一下。欢迎大佬们来带带~_

1. 更新子模块 `git submodule update --init --recursive`
2. 下载 MaaFramework 的 [Release 包](https://github.com/MaaAssistantArknights/MaaFramework/releases)，解压到 `source/cli/x64/Release`
3. 使用 Visual Studio 编译 `source/cli/MAA1999_CLI.sln`
4. `tools/CropRoi` 是个小工具，可以用来裁剪图片和获取 ROI

## Join us

开发 QQ 群：649344857
