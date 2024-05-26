import logging
import logging.handlers
import sys
from logging import Logger


def get_logger(name: str) -> Logger:
    logger = logging.getLogger(name)
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(message)s",
            datefmt=r"%Y-%m-%dT%H:%M:%S",
        )
    )
    logger.addHandler(h)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


__all__ = ("get_logger", "Logger")
