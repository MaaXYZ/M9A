# M9A

基于全新架构的 亿韭韭韭 小助手。图像技术 + 模拟控制，解放双手！  
由 [MaaFramework](https://github.com/MaaAssistantArknights/MaaFramework) 强力驱动！

## 画大饼

- [x] 自动收菜  
  最基本的了，没啥好说的。目前已支持 全关卡导航刷关 + 可配置吃糖 + 签到 + 收荒原 + 每日心相 + 领邮件和日常。
- [ ] 关卡掉落识别  
  有佬在搓类似企鹅的站点了：[圣洛夫数据部](https://github.com/St-Pavlov-Data-Department)，欢迎加入！
- [ ] 仓库识别 + 材料需求计算 + 关卡导航  
  粥 MAA 没完成的事情，就由我 韭 MAA 来完成（bushi
- [ ] ~~自动战斗~~  
  ~~韭的战斗有点小难度，但又没粥那么难。我觉得完全可以做到打的比大多数玩家水平高，纯粹的无感情的概率 + 数值机器。~~  
  游戏自带了，摸！

## 图形化界面

目前暂无正式版 GUI，但有以下由社区大佬们贡献的 GUI 项目，欢迎使用！

- [MAA1999WPF](https://github.com/MLAcookie/MAA1999WPF) 拿WPF框架写的一个MAA199的UI
- [MaaY](https://github.com/MaaAssistantArknights/MaaY) 为MaaFramework重新设计的通用界面

## How to build

**如果你要编译源码才看这节，否则直接 [下载](https://github.com/MaaAssistantArknights/M9A/releases) 即可**

0. 完整克隆本项目及子项目

    ```bash
    git clone https://github.com/MaaAssistantArknights/MaaFramework.git
    git submodule update --init --recursive
    ```

1. 下载 MaaFramework 的 [Release 包](https://github.com/MaaAssistantArknights/MaaFramework/releases)，解压到 `deps` 文件夹中
2. 安装

    ```python
    python ./install.py
    ```

生成的二进制及相关资源文件在 `install` 目录下

## 开发相关

- `tools/ImageCropper` 可以用来裁剪图片和获取 ROI
- Pipeline 协议请参考 [MaaFramework 的文档](https://github.com/MaaAssistantArknights/MaaFramework/blob/main/docs/zh_cn/3.1-%E4%BB%BB%E5%8A%A1%E6%B5%81%E6%B0%B4%E7%BA%BF%E5%8D%8F%E8%AE%AE.md)

## Join us

开发 QQ 群：649344857
