import os
import time
import json
from datetime import datetime, timedelta

import pytz
from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from utils import logger


@AgentServer.custom_action("BankPurchaseRecord")
class BankPurchaseRecord(CustomAction):
    """
    记录在银行购买物品的时间戳

    参数格式:
    {
        "item": "物品名称"
    }
    """

    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:

        item = json.loads(argv.custom_action_param)["item"]

        with open("config/m9a_data.json") as f:
            data = json.load(f)

        data["bank"][item] = int(time.time() * 1000)

        with open("config/m9a_data.json", "w") as f:
            json.dump(data, f, indent=4)

        logger.info(f"{item}检查时间已记录")

        return CustomAction.RunResult(success=True)


@AgentServer.custom_action("ModifyBankTaskList")
class ModifyBankTaskList(CustomAction):
    """
    这时的任务链在ui执行后已经禁止了不运行的任务，这步是通过读本地过往执行记录继续禁止不需要运行的任务。

    参数格式:
    {
        "resource": "cn/en/jp"
    }
    """

    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:

        tasks: dict = {
            "FreeWeeklyGift": "week",
            "Rabbit": "month",
            "SmallGlobe": "month",
            "TinyGlobe": "month",
            "Gluttony": "month",
            "TinyGlobe(1)": "month",
            "ResonantCassette": "month",
            "GoldenMelonSeeds": "week",
            "OriginalChicken": "month",
            "Fries": "month",
        }
        resource = json.loads(argv.custom_action_param)["resource"]

        if resource == "cn":
            timezone = "Asia/Shanghai"
        elif resource == "en":
            timezone = "America/New_York"
        else:
            timezone = "Asia/Tokyo"

        file_path = "config/m9a_data.json"
        default_data = {"bank": {}}

        if not os.path.exists(file_path):

            logger.warning("config/m9a_data.json 不存在，正在初始化")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(default_data, file, indent=4)
            logger.info("初始化完成，跳过时间检查")

            return CustomAction.RunResult(success=True)

        with open(file_path) as f:
            data = json.load(f)

        if "bank" not in data:
            data["bank"] = {}
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, f, indent=4)
            logger.info("无时间记录，跳过时间检查")

            return CustomAction.RunResult(success=True)

        for task, type in tasks.items():
            is_current_week, is_current_month = self.is_current_period(
                data["bank"].get(task, 1058306766000), timezone
            )
            if type == "week":
                if is_current_week:
                    context.override_pipeline({f"{task}": {"enabled": False}})
                    logger.info(f"{task} 本周已完成，跳过")
            elif type == "month":
                if is_current_month:
                    context.override_pipeline({f"{task}": {"enabled": False}})
                    logger.info(f"{task} 本月已完成，跳过")

        return CustomAction.RunResult(success=True)

    def is_current_period(self, timestamp_ms, timezone="Asia/Shanghai"):
        """
        判断毫秒级时间戳是否在当前周和当前月

        参数:
            timestamp_ms: 毫秒级时间戳
            timezone: 时区字符串，默认为"Asia/Shanghai"（北京时间）

        返回:
            tuple: (is_current_week, is_current_month)
        """

        tz = pytz.timezone(timezone)

        timestamp_datetime = datetime.fromtimestamp(timestamp_ms / 1000.0, tz)

        now = datetime.now(tz)

        # 计算当前周的开始（本周或上周一05:00:00）
        # Python中，weekday()返回0-6，0是周一，6是周日
        days_since_monday = now.weekday()  # 距离最近过去的周一的天数

        # 计算到本周一的天数
        week_start = now.replace(hour=5, minute=0, second=0, microsecond=0) - timedelta(
            days=days_since_monday
        )

        # 如果当前时间早于周一5点，则使用上周一作为周期开始
        if now.weekday() == 0 and now.hour < 5:  # 如果是周一且不到5点
            week_start = week_start - timedelta(days=7)  # 使用上周一

        # 计算下周一05:00:00作为本周结束
        week_end = week_start + timedelta(days=7)

        # 计算当前月的开始（当月1号05:00:00）
        if now.day == 1 and now.hour < 5:
            # 如果是1号但不到5点，使用上个月1号作为开始
            if now.month == 1:
                month_start = datetime(now.year - 1, 12, 1, 5, 0, 0, 0, tzinfo=tz)
            else:
                month_start = datetime(
                    now.year, now.month - 1, 1, 5, 0, 0, 0, tzinfo=tz
                )
        else:
            # 否则使用本月1号
            month_start = now.replace(day=1, hour=5, minute=0, second=0, microsecond=0)
            # 如果已经过了1号5点，但当前日期小于1号，则需要往前调整一个月
            if now.day < 1 or (now.day == 1 and now.hour < 5):
                if month_start.month == 1:
                    month_start = month_start.replace(
                        year=month_start.year - 1, month=12
                    )
                else:
                    month_start = month_start.replace(month=month_start.month - 1)

        # 计算下个月1号05:00:00作为当月结束
        if month_start.month == 12:
            month_end = datetime(month_start.year + 1, 1, 1, 5, 0, 0, 0, tzinfo=tz)
        else:
            month_end = datetime(
                month_start.year, month_start.month + 1, 1, 5, 0, 0, 0, tzinfo=tz
            )

        # 判断是否在当前周和当前月
        is_current_week = week_start <= timestamp_datetime < week_end
        is_current_month = month_start <= timestamp_datetime < month_end

        return is_current_week, is_current_month
