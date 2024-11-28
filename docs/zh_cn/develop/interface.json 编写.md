# interface.json 编写

[参考资料——interface.schema.json](https://github.com/MaaXYZ/MaaFramework/blob/main/tools/interface.schema.json)

interface.json

## controller

对于 M9A 来说，固定选择 adb 方式，基本不需要改动。

## resource

资源配置。每种资源需要资源名 `name` 以及 资源路径 `path`，均为必填。

特别地，对于资源路径 'path'，M9A 按顺序加载资源，若是存在相同资源名，则后加载的资源会覆盖前面的资源。

以 B 服为例，资源配置如下：

```json
{
  "resources": [
        {
            "name": "B 服",
            "path": [
                "{PROJECT_DIR}/resource/base",
                "{PROJECT_DIR}/resource/bilibili"
            ]
        }
}
```

这里，`{PROJECT_DIR}` 是 M9A 项目根目录，`base` 文件夹是官服资源，`bilibili` 文件夹是 B 服覆盖官服的资源。

## task

任务列表。任务列表包含多个任务，而每个任务又有任务名 `name`、任务入口 `entry`、任务参数 `pipeline_override`、以及任务选项 `option`，其中 `name` `entry` 必填。

`pipeline_override` 中应为 pipeline task，并带有覆写参数，例如：

```json
{
    "name": "轶事派遣（角色故事请自行阅读）",
    "entry": "Anecdote",
    "pipeline_override": {
        "EnterTheActivityMain": {
            "template_doc": "修改为当期活动入口的template",
            "template": "Combat/Activity/LondonDawningEnterTheShow.png"
        }
}
```

这里原task为：

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

经过覆写，该 task 在执行“轶事派遣（角色故事请自行阅读）”任务时，实际执行效果等同于：

```json
{
    "EnterTheActivityMain": {
        "recognition": "TemplateMatch",
        "template": "Combat/Activity/LondonDawningEnterTheShow.png",
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

执行“轶事派遣（角色故事请自行阅读）”任务后，task 便会恢复原状。

`option` 则是根据你下面的具体设置来决定如何覆写 pipeline task。

## option

选项定义。每种选项有可选项 `cases` 以及 默认选项 `default_case`, 其中`cases`必填。

一般用 `cases`,举例：

```json
{
    "task": [
        {
            "name": "常规作战",
            "entry": "Combat",
            "option": [
                "作战关卡",
                "复现次数",
                "刷完全部体力",
                "吃全部临期糖"
            ]
        }
    ],
    "option":{
        "刷完全部体力": {
            "cases": [
                {
                    "name": "Yes",
                    "pipeline_override": {
                        "AllIn": {
                            "enabled": true
                        }
                    }
                },
                {
                    "name": "No",
                    "pipeline_override": {
                        "AllIn": {
                            "enabled": false
                        }
                    }
                }
            ]
        }
    }
}

## version

版本。不必填写，ci install 时会自动生成。

## message

信息。目前为 MaaPiCli 运行时第一行输出的文字。
