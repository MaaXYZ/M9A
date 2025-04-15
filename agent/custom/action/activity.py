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
    判断当前是否在作战开放期间

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

        for key in reversed(list(data.keys())):
            item = data[key]
            if now < item["activity"]["combat"]["end_time"]:
                if now > item["activity"]["combat"]["start_time"]:
                    if item["activity"]["combat"]["event_type"] == "MainStory":
                        context.override_next("JudgeDuringAct", [])
                        logger.info(f"当前主线版本：{key} {item['version_name']}")
                        logger.info(
                            f"距离版本结束还剩 {ms_timestamp_diff_to_dhm(now, item['end_time'])}，跳过当前任务"
                        )
                        return CustomAction.RunResult(success=True)
                    logger.info(f"当前版本：{key} {item['version_name']}")
                    logger.info(
                        f"距离作战结束还剩 {ms_timestamp_diff_to_dhm(now, item['activity']['combat']['end_time'])}"
                    )
                    context.override_pipeline(
                        {
                            "JudgeDuringRe_release": {
                                "custom_action_param": {"resource": resource}
                            }
                        }
                    )
                    return CustomAction.RunResult(success=True)
                continue
            break

        context.override_next("JudgeDuringAct", [])
        logger.info("当前不在活动时间内，跳过当前任务")
        return CustomAction.RunResult(success=True)


@AgentServer.custom_action("DuringAnecdote")
class DuringAnecdote(CustomAction):
    """
    判断当前是否在轶事开放期间

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

        for key in reversed(list(data.keys())):
            item = data[key]
            if now < item["activity"]["anecdote"]["end_time"]:
                if now > item["activity"]["anecdote"]["start_time"]:
                    logger.info(f"当前版本：{key} {item['version_name']}")
                    logger.info(
                        f"距离轶事结束还剩 {ms_timestamp_diff_to_dhm(now, item['activity']['anecdote']['end_time'])}"
                    )
                    return CustomAction.RunResult(success=True)
                continue
            break

        context.override_pipeline({"Anecdote": {"next": [], "interrupt": []}})
        logger.info("当前不在轶事开放时间，跳过当前任务")

        return CustomAction.RunResult(success=True)


@AgentServer.custom_action("DuringRe_release")
class DuringRe_release(CustomAction):
    """
    判断当前是否在版本复刻期间

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

        for key in reversed(list(data.keys())):
            item = data[key]
            if item["activity"].get("re-release"):
                if now < item["activity"]["re-release"]["end_time"]:
                    if now > item["activity"]["re-release"]["start_time"]:
                        logger.info(
                            f"当前复刻活动：{item['activity']['re-release']['name']}"
                        )
                        logger.info(
                            f"距离复刻作战结束还剩 {ms_timestamp_diff_to_dhm(now, item['activity']['re-release']['end_time'])}"
                        )
                        context.override_pipeline(
                            {
                                "ActivityRe_releaseChapter": {
                                    "custom_recognition_param": {
                                        "Re_release_name": item["activity"][
                                            "re-release"
                                        ]["alias"]
                                    }
                                }
                            }
                        )
                        return CustomAction.RunResult(success=True)
                    continue
                break

        context.override_pipeline(
            {"JudgeDuringRe_release": {"next": [], "interrupt": []}}
        )
        logger.info("当前不在复刻作战开放时间，跳过当前任务")
        return CustomAction.RunResult(success=True)
