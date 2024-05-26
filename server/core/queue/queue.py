from __future__ import annotations

import time
from types import TracebackType
from typing import Self

import pika

from server.core.settings import get_settings

from .type import (
    BasicDeliver,
    BasicProperties,
    BlockingChannel,
    ICallBack,
    QueueMessage,
)

settings = get_settings()


class QueueClient:
    TOPIC_EXCHANGE_TYPE = "topic"

    def __init__(self: Self):
        self._active_connection = False
        self._active_consumer = False

    def _queue_connection(self: Self):
        if self._active_connection is False:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.queue_host,
                    port=settings.queue_port,
                    credentials=pika.PlainCredentials(
                        username=settings.queue_username,
                        password=settings.queue_password,
                    ),
                )
            )
            self._active_connection = True
            self._channel = self._connection.channel()
            self._channel.queue_declare(queue=settings.queue_name, durable=True)

    def _callback(
        self: Self,
        callback: ICallBack,
        callback_fail: ICallBack | None = None,
        retry: int = 1,
    ):
        def wrapper(
            channel: BlockingChannel,
            method: BasicDeliver,
            properties: BasicProperties,
            body: bytes,
        ):
            message = QueueMessage(
                channel=channel,
                method=method,
                properties=properties,
                body=body,
                client=self,
            )
            error: Exception | None = None
            for n in range(retry):
                try:
                    callback(message)
                    error = None
                    break
                except Exception as err:
                    error = err
                    time.sleep(n + 1.001)
            try:
                if error:
                    if callback_fail is None:
                        raise error
                    message.error = error
                    callback_fail(message)
            finally:
                channel.basic_ack(delivery_tag=method.delivery_tag)

        return wrapper

    def __enter__(self: Self) -> Self:
        self._queue_connection()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        try:
            if exc_val:
                raise exc_val
        finally:
            self.close()

    def consumer(
        self: Self,
        callback: ICallBack,
        callback_fail: ICallBack | None = None,
        retry: int = 1,
    ):
        if self._active_consumer is False:
            self._queue_connection()
            self._channel.basic_qos(prefetch_count=1)
            self._channel.basic_consume(
                queue=settings.queue_name,
                on_message_callback=self._callback(
                    callback=callback,
                    callback_fail=callback_fail,
                    retry=retry,
                ),
            )
            self._active_consumer = True
            self._channel.start_consuming()

    def producer(self: Self, message: str):
        self._queue_connection()
        self._channel.exchange_declare(
            exchange=settings.queue_exchange, exchange_type=self.TOPIC_EXCHANGE_TYPE
        )
        self._channel.queue_bind(
            exchange=settings.queue_exchange,
            queue=settings.queue_name,
            routing_key=settings.queue_routing_key,
        )
        self._channel.basic_publish(
            exchange=settings.queue_exchange,
            routing_key=settings.queue_routing_key,
            body=message,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )

    def close(self: Self):
        if self._active_consumer is True:
            self._channel.stop_consuming()
            self._active_consumer = False
        self._connection.close()
        self._active_connection = False


__all__ = ("QueueClient",)
