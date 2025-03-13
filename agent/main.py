import os
import sys

from maa.agent.agent_server import AgentServer
from maa.toolkit import Toolkit

# 将当前目录添加到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from custom import *
from utils import logger


def main():
    Toolkit.init_option("./")

    socket_id = sys.argv[-1]

    AgentServer.start_up(socket_id)
    logger.info("AgentSever 启动")
    AgentServer.join()
    AgentServer.shut_down()
    logger.info("AgentSever 关闭")


if __name__ == "__main__":
    main()
