import random
import threading
import time

from server.core import logging
from server.core.queue import QueueMessage

logger = logging.get_logger("ConsumerService")


def processor(message: QueueMessage):
    sleep = random.randint(3, 9)
    logger.info(
        f"{threading.get_native_id()!s} | PROCESSOR : {message.text} | SLEEP : {sleep!s}s"
    )
    if (sleep % 3) == 0:
        raise Exception("test fail")
    time.sleep(sleep + 0.001)


def processor_fail(message: QueueMessage):
    logger.info(
        f"{threading.get_native_id()!s} | FAIL .....: {message.text} | ERROR : {message.error!r}"
    )
