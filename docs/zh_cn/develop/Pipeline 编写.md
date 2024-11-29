# Pipeline 编写

## 编写规范

### 命名规范

为保证资源的美观一致，请遵循以下原则。

#### 资源命名

- 对于图片等文件，采用大驼峰命名法，所有单词的首字母都大写。
- 对于 `pipeline.json` 文件，一般来说，采用蛇形命名法，单词之间用下划线分隔，所有字母小写，特别地，专有名词的活动采取大驼峰命名法，一般在 `activity` 内。
- 对于 `image` 下文件夹，每个文件夹对应一个 `pipeline.json` 文件，文件夹名采用大驼峰命名法，特别地，`activity` 内 `pipeline.json` 对应的 `image` 放到 `Combat/Activity` 处。

#### task 命名

大多数采用大驼峰命名法，特别地，部分情况下用 `_` 连接前、后缀。

前缀一般为 `Sub` 或 当前活动缩写（如 `SOD` 黄昏的音序、`EITM` 山麓的回音）等，其他情况建议不要前缀。

后缀一般为 `数字` 或 `状态` 等，表示该任务的具体阶段或状态。（建议新写的任务不加后缀）

### task 编写

参考[Pipeline 协议详细说明](https://github.com/MaaXYZ/MaaFramework/blob/main/docs/zh_cn/3.1-%E4%BB%BB%E5%8A%A1%E6%B5%81%E6%B0%B4%E7%BA%BF%E5%8D%8F%E8%AE%AE.md)

> [!NOTE]
>
> - 一般 `next` 放置当前任务的出口任务，`interrupt` 放置当前任务的中断任务。
> - 为了保证任务的环环相扣，建议多写些 `Flag` 任务进行判断。
> - 在 `next` 加入自身可提高任务的稳定性。（存在程序未正确接受动作的情况）

### next & interrupt 任务顺序

总体上，`interrupt` 第一个任务 比 `next` 最后一个任务低一优先级。

在 `next` 或 `interrupt` 内部，统一先按照优先级由高到低顺序排列，不能出现优先级倒挂的情况。（现有判断一个小弹窗的任务B，和判断跳出弹窗前界面的任务A。如果弹窗出现时依旧能匹配到任务A，则任务B的优先级应该高于任务A，否则会出现无法处理B而卡死于A的情况）

同一优先级内的任务，可按照匹配频率由高到低顺序排列，以便提高命中率，降低资源消耗。

### 注释规范

注释共两种：

1. `.*_doc$|^doc$`： 以 _doc 结尾的字符串或者正好是 doc 的字符串。
2. `.*_code$|^code$`：以 _code 结尾的字符串或者正好是 code 的字符串。

前者为对当前 task（或某字段）的说明，后者为对必填字段的占位。举例：

```json
{
    "EnterTheActivityMain": {
        "doc": "进入当期活动主界面",
        "template_code": "在interface.json中修改template",
        "recognition": "TemplateMatch",
        "roi": [
            885,
            123,
            340,
            183
        ],
        "action": "Click",
        "post_wait_freezes": 300,
        "next": [
            "ActivityMainFlag",
            "EnterTheActivityMain"
        ]
    }
}
```

`doc` 为当前 task 说明。

`template_code` 为必填字段占位，
原因是 `recognition` 为 `TemplateMatch` 时， "template" 字段必填，但我们想在 `interface.json` 中修改，故用 `template_code` 占位。
