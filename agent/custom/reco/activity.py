import json
from typing import Union, Optional

from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context
from maa.define import RectType


@AgentServer.custom_recognition("ActivityRe_releaseChapter")
class ActivityRe_releaseChapter(CustomRecognition):
    """
    识别复刻活动对应别名

    参数格式：
    {
        "Re_release_name": "alias"
    }
    """

    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> Union[CustomRecognition.AnalyzeResult, Optional[RectType]]:

        expected = json.loads(argv.custom_recognition_param)["Re_release_name"]
        reco_detail = context.run_recognition("ActivityLeftList", argv.image)

        if reco_detail is None:
            return CustomRecognition.AnalyzeResult(box=None, detail="无文字")

        for result in reco_detail.all_results:
            if expected in result.text:
                return CustomRecognition.AnalyzeResult(box=result.box, detail=expected)

        return CustomRecognition.AnalyzeResult(box=None, detail="无目标")
