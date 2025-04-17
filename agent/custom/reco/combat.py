from typing import Union, Optional

from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context
from maa.define import RectType

from utils import logger


@AgentServer.custom_recognition("StagePromotionComplete")
class StagePromotionComplete(CustomRecognition):
    """
    推图模式完成判断（当前关为满星且无下一关）
    """

    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> Union[CustomRecognition.AnalyzeResult, Optional[RectType]]:

        cur_flag = False
        reco_detail = context.run_recognition(
            "StagePromotionCurStageComplete", argv.image
        )
        if reco_detail is not None:
            if reco_detail.best_result:
                cur_flag = True
        else:
            reco_detail = context.run_recognition(
                "StagePromotionCurStageComplete",
                argv.image,
                {
                    "StagePromotionCurStageComplete": {
                        "lower": [201, 38, 38],
                        "upper": [221, 58, 58],
                    }
                },
            )
            if reco_detail is not None:
                if reco_detail.best_result:
                    cur_flag = True
        if cur_flag:
            reco_detail = context.run_recognition(
                "StagePromotionClickNextStage", argv.image
            )
            if reco_detail is not None:
                if not reco_detail.best_result:
                    return [0, 0, 0, 0]
        return None
