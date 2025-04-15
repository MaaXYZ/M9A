from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from utils import logger


@AgentServer.custom_action("SummonlngSwipe")
class SummonlngSwipe(CustomAction):
    """
    分派魔精滑动名片。
    """

    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:

        img = context.tasker.controller.post_screencap().wait().get()

        reco_first = context.run_recognition("SummonlngCardFirst", img)
        reco_last = context.run_recognition("SummonlngCardLast", img)

        if reco_first is None or reco_last is None:
            return CustomAction.RunResult(success=True)
        x1, y1, x2, y2 = (
            int(reco_first.best_result.box[0] + reco_first.best_result.box[2] / 2),
            int(reco_first.best_result.box[1] + reco_first.best_result.box[3] / 2),
            int(reco_last.best_result.box[0] + reco_last.best_result.box[2] / 2),
            int(reco_last.best_result.box[1] + reco_last.best_result.box[3] / 2),
        )
        context.tasker.controller.post_swipe(x1, y1, x2, y2, duration=1000).wait()

        return CustomAction.RunResult(success=True)
