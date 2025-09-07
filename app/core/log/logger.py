from typing import Literal

import logging


logger_parent = logging.getLogger("my_logger")


def configure_logging(log: logging.Logger,
                      level: Literal[10, 20, 30, 40, 50]) -> None:
    formatter = logging.Formatter(fmt="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)s - %(message)s",
                                  datefmt="%Y-%m-%d %H:%M:%S")

    handler = logging.StreamHandler()
    handler.setFormatter(fmt=formatter)

    log.setLevel(level)
    log.addHandler(handler)
