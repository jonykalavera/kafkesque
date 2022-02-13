from contextlib import asynccontextmanager
from typing import Optional
from django.core.handlers.asgi import logger
import logging
from channels.consumer import AsyncConsumer
import json
from confluent_kafka import Consumer as ConsumerClient, Message
import httpx

from consumers.schemas import StartConsumerSchema


logger = logging.getLogger(__name__)


class KafkaConsumerConsumer(AsyncConsumer):
    @asynccontextmanager
    async def _consumer_client(self, cmd):
        try:
            client = ConsumerClient(**cmd.cluster["config"])
            client.subscribe(cmd.topics.split(","))
            logger.info("Subscribed to:", cmd.topics)
            yield client
        finally:
            client.close()

    async def _loop_messages(self, cmd):
        async with self._consumer_client(cmd) as client:
            while True:
                msg: Optional[Message] = client.poll(0.1)
                if msg is None:
                    continue
                if msg.error():
                    print("Consumer error: {}".format(msg.error()))
                    continue
                key = msg.key()
                value = msg.value().decode("utf-8")
                yield key, value

    async def kafka_start_consumer(self, config: dict):
        cmd = StartConsumerSchema(*config)
        for key, value in self._loop_messages(cmd):
            logger.info("Received message: %s: %s", key, value)
            if cmd.webhook_url:
                self.send(
                    "kafka-consumer",
                    {"type": "push.to.webhook", "key": key, "value": json.loads(value)},
                )

    async def push_to_webhook(self, message):
        webhook = message.pop("webhook")
        httpx.post(
            webhook,
            data={
                "key": message.get("key"),
                "value": message["value"],
            },
        )
