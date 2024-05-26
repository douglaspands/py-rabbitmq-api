from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Self, TypeAlias

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic as PikaBasic
from pika.spec import BasicProperties

BasicDeliver: TypeAlias = PikaBasic.Deliver

if TYPE_CHECKING:
    from .queue import QueueClient


@dataclass
class QueueMessage:
    client: QueueClient
    channel: BlockingChannel
    method: BasicDeliver
    properties: BasicProperties
    body: bytes
    error: Exception | None = None

    @property
    def text(self: Self) -> str:
        return self.body.decode("utf8")

    @property
    def to_dict(self: Self) -> dict[str, Any]:
        return json.loads(self.body)


ICallBack: TypeAlias = Callable[[QueueMessage], None]

__all__ = (
    "BlockingChannel",
    "BasicDeliver",
    "BasicProperties",
    "QueueMessage",
    "ICallBack",
)
