import json
from os import makedirs
from datetime import datetime

from PIL import Image
from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context


@AgentServer.custom_action("Screenshot")
class Screenshot(CustomAction):

    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:

        # image array(BGR)
        screen_array = context.tasker.controller.post_screencap().wait().get()

        # BGR2RGB
        if len(screen_array.shape) == 3 and screen_array.shape[2] == 3:
            rgb_array = screen_array[:, :, ::-1]
        else:
            rgb_array = screen_array

        img = Image.fromarray(rgb_array)

        save_dir = json.loads(argv.custom_action_param)["save_dir"]
        makedirs(save_dir, exist_ok=True)
        img.save(f"{save_dir}/{self._get_format_timestamp()}.png")

        return CustomAction.RunResult(success=True)

    def _get_format_timestamp(self):

        now = datetime.now()

        date = now.strftime("%Y.%m.%d")
        time = now.strftime("%H.%M.%S")
        milliseconds = f"{now.microsecond // 1000:03d}"

        return f"{date}-{time}.{milliseconds}"
