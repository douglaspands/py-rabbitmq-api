import json
from datetime import datetime
from uuid import uuid4

from typer import Typer

from server.core import logging
from server.core.queue.queue import QueueClient

logger = logging.get_logger(__name__)
app = Typer(name="producer")


@app.command(name="send", help="producer send message")
def producer_send(message: str):
    data = {"data": message, "correlation_id": uuid4(), "created_at": datetime.now()}
    with QueueClient() as client:
        client.producer(message=json.dumps(data, default=str))
    logger.info(f" [x] Sent {data!r}")


@app.command(name="sends", help="producer sends messages")
def producer_sends(message: str, count: int = 1):
    with QueueClient() as client:
        for n in range(count):
            data = {
                "data": f"{n:>2d}_{message}",
                "correlation_id": uuid4(),
                "created_at": datetime.now(),
            }
            client.producer(message=json.dumps(data, default=str))
            logger.info(f" [x] Sent {data!r}")


__all__ = ("app",)
