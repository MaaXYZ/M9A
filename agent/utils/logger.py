import os
import sys

from loguru import logger


def setup_logger(log_dir="debug/custom"):

    os.makedirs(log_dir, exist_ok=True)

    logger.remove()

    logger.add(
        sys.stderr,
        format="[<level>{level}</level>] <level>{message}</level>",
        colorize=True,
        level="INFO",
    )

    logger.add(
        f"{log_dir}/{{time:YYYY-MM-DD}}.log",
        rotation="00:00",  # midnight
        retention="2 weeks",
        compression="zip",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
        encoding="utf-8",
        enqueue=True,
    )

    return logger


custom_logger = setup_logger()
