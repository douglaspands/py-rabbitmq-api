from threading import Thread
from typing import Self

from typer import Typer

from server.core import logging
from server.core.queue import ICallBack, QueueClient

app = Typer(name="consumer")


class ConsumerWorkerThread(Thread):
    def __init__(
        self: Self,
        callback: ICallBack,
        callback_fail: ICallBack | None = None,
        retry: int = 1,
    ):
        super().__init__(daemon=True)
        self._retry = retry
        self._callback = callback
        self._callback_fail = callback_fail

    def run(self: Self):
        with QueueClient() as client:
            client.consumer(
                callback=self._callback,
                callback_fail=self._callback_fail,
                retry=self._retry,
            )


class ConsumerWorker:
    def __init__(
        self: Self,
        callback: ICallBack,
        callback_fail: ICallBack | None = None,
        workers: int = 1,
        retry: int = 1,
    ):
        self._consumers: list[ConsumerWorkerThread] = []
        for _ in range(workers):
            t = ConsumerWorkerThread(
                callback=callback,
                callback_fail=callback_fail,
                retry=retry,
            )
            self._consumers.append(t)

    def run(self: Self):
        logger = logging.get_logger("ConsumerWorker")
        logger.info(" [*] Waiting for messages. To exit press CTRL+C")
        try:
            for c in self._consumers:
                c.start()
            for c in self._consumers:
                c.join()
        except KeyboardInterrupt:
            logger.warning(" [*] User interrupted")


__all__ = ("ConsumerWorker",)
