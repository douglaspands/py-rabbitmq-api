from typer import Typer

from server.core.consumer import ConsumerWorker
from server.core.queue import QueueMessage
from server.services import consumer_service

app = Typer(name="consumer")


@app.command(name="start", help="consumer worker start")
def consumer_start(workers: int = 1, retry: int = 1):
    consumer_worker = ConsumerWorker(
        callback=callback,
        callback_fail=callback_fail,
        workers=workers,
        retry=retry,
    )
    consumer_worker.run()


def callback(
    message: QueueMessage,
):
    consumer_service.processor(message=message)


def callback_fail(
    message: QueueMessage,
):
    consumer_service.processor_fail(message=message)


__all__ = ("app",)
