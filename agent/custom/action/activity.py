import time
import json

from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from utils import logger
from utils import ms_timestamp_diff_to_dhm


@AgentServer.custom_action("DuringAct")
class DuringAct(CustomAction):
    """
    判断当前是否在活动期间

    参数格式：
    {
        "resource": "cn/en/jp"
    }
    """

    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:

        resource = json.loads(argv.custom_action_param)["resource"]

        with open(f"resource/{resource}.json", encoding="utf-8") as f:
            data = json.load(f)

        now = int(time.time() * 1000)

        last_key = list(data.keys())[-1]
        if now > data[last_key]["activity"]["combat"]["end_time"]:
            context.override_pipeline(
                {
                    "ActivityEntry": {
                        "next": [],
                        "interrupt": [],
                        "focus": True,
                        "focus_tip": "当前不在作战时间内，跳过当前任务",
                    }
                }
            )
            logger.info("当前不在活动时间内，跳过当前任务")
            return CustomAction.RunResult(success=True)

        for key in reversed(list(data.keys())):
            item = data[key]
            if now > item["activity"]["combat"]["start_time"]:
                if item["activity"]["combat"]["event_type"] == "MainStory":
                    logger.info(f"当前主线版本：{key} {item['version_name']}")
                    logger.info(
                        f"距离版本结束还剩 {ms_timestamp_diff_to_dhm(now, item['end_time'])}，跳过当前任务"
                    )
                    return CustomAction.RunResult(success=True)
                logger.info(f"当前版本：{key} {item['version_name']}")
                logger.info(
                    f"距离作战结束还剩 {ms_timestamp_diff_to_dhm(now, item['activity']['combat']['end_time'])}"
                )
                return CustomAction.RunResult(success=True)

        logger.error("没有当前版本信息")
        return CustomAction.RunResult(success=False)
