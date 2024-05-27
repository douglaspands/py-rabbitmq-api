from __future__ import annotations

import time
from types import TracebackType
from typing import Self, Type

import pika

from .type import (
    BasicDeliver,
    BasicProperties,
    BlockingChannel,
    ICallBack,
    QueueMessage,
)


class QueueClient:
    TOPIC_EXCHANGE_TYPE = "topic"

    def __init__(
        self: Self,
        host: str,
        queue_name: str,
        port: str = "5672",
        exchange: str | None = None,
        routing_key: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ):
        self._queue_host = host
        self._queue_name = queue_name
        self._queue_port = port
        self._queue_exchange = exchange
        self._queue_routing_key = routing_key
        self._queue_username = username
        self._queue_password = password
        # Flags
        self._active_connection = False
        self._active_consumer = False
        self._active_producer = False

    def _queue_connection(self: Self):
        if self._active_connection is False:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self._queue_host,
                    port=self._queue_port,
                    credentials=pika.PlainCredentials(
                        username=self._queue_username,
                        password=self._queue_password,
                    ),
                )
            )
            self._channel = self._connection.channel()
            self._channel.queue_declare(queue=self._queue_name, durable=True)
            self._active_connection = True

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
                queue=self._queue_name,
                on_message_callback=self._callback(
                    callback=callback,
                    callback_fail=callback_fail,
                    retry=retry,
                ),
            )
            self._active_consumer = True
            self._channel.start_consuming()

    def producer(self: Self, message: str):
        if self._active_producer is False:
            self._queue_connection()
            self._channel.exchange_declare(
                exchange=self._queue_exchange, exchange_type=self.TOPIC_EXCHANGE_TYPE
            )
            self._channel.queue_bind(
                exchange=self._queue_exchange,
                queue=self._queue_name,
                routing_key=self._queue_routing_key,
            )
            self._active_producer = True
        self._channel.basic_publish(
            exchange=self._queue_exchange,
            routing_key=self._queue_routing_key,
            body=message,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )

    def close(self: Self):
        self._active_producer = False
        if self._active_consumer is True:
            self._channel.stop_consuming()
            self._active_consumer = False
        self._connection.close()
        self._active_connection = False

    @classmethod
    def create_by_settings(cls: Type[QueueClient]) -> QueueClient:
        from server.core.settings import get_settings

        settings = get_settings()
        return cls(
            host=settings.queue_host,
            port=settings.queue_port,
            queue_name=settings.queue_name,
            exchange=settings.queue_exchange,
            routing_key=settings.queue_routing_key,
            username=settings.queue_username,
            password=settings.queue_password,
        )


__all__ = ("QueueClient",)
