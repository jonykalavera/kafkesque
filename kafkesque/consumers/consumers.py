from typing import Optional
from django.core.handlers.asgi import logger
import logging
from channels.consumer import AsyncConsumer
import json
from confluent_kafka import Consumer, Message
import httpx
from django.conf import settings


logger = logging.getLogger(__name__)


class KafkaConsumerConsumer(AsyncConsumer):
    async def kafka_consume(self, config):
        name = config["name"]
        webhook = config.get("webhook")
        auto_offset_reset = config.get("auto.offset.reset", "earliest")
        topics = config["topics"]

        c = Consumer(
            {
                "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
                "group.id": name,
                "auto.offset.reset": auto_offset_reset,
            }
        )
        c.subscribe(topics)
        print("Subscribed to:", topics)
        while True:
            msg: Optional[Message] = c.poll(0.1)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            key = msg.key()
            value = msg.value().decode("utf-8")
            print("Received message: {}".format(msg.value().decode("utf-8")))
            if webhook:
                self.send(
                    "kafka-consume",
                    {"type": "push.to.webhook", "key": key, "value": json.loads(value)},
                )

        c.close()

    async def push_to_webhook(self, message):
        webhook = message.pop("webhook")
        httpx.post(
            webhook,
            data={
                "key": message.get("key"),
                "value": message["value"],
            },
        )
