import os
from django.core.handlers.asgi import logger
import logging
from channels.consumer import AsyncConsumer
import json
from confluent_kafka import Consumer
import httpx

logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', '192.168.178.25:9093')

class KafkaConsumerConsumer(AsyncConsumer):
    async def kafka_consume(self, config):
        name = config['name']
        webhook = config.get('webhook')
        auto_offset_reset = config.get('auto.offset.reset', 'earliest')
        topics = config['topics']

        c = Consumer({
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
            'group.id': name,
            'auto.offset.reset': auto_offset_reset
        })
        c.subscribe(topics)
        print("Subscribed to:", topics)
        while True:
            msg = c.poll(0.1)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            value = msg.value().decode('utf-8')
            print('Received message: {}'.format(msg.value().decode('utf-8')))
            if webhook:
                httpx.post(webhook, data={
                    # "key": msg.key().decode('utf-8'),
                    "value": json.loads(value),
                })
        c.close()
