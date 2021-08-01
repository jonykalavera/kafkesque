import os
import logging
from channels.consumer import AsyncConsumer
import json
from confluent_kafka import Consumer
import httpx
from redis import Redis
import asyncio


logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', '192.168.178.25:9093')
REDIS_CLIENT = Redis()


class KafkaConsumerConsumer(AsyncConsumer):
    async def kafka_consume(self, config):
        name = config['name']
        webhook = config.get('webhook')
        auto_offset_reset = config.get('auto.offset.reset', 'earliest')
        topics = config['topics']

        consumer = Consumer({
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
            'group.id': name,
            'auto.offset.reset': auto_offset_reset
        })
        consumer.subscribe(topics)
        print("Subscribed to:", topics)

        # Run dispatcher
        asyncio.run(run_dispatcher(topics))

        # Run consumer
        run_consumer(consumer, topics, webhook)


async def run_dispatcher(topics):
    while True:
        msg = REDIS_CLIENT.rpop(topics)
        if msg is None:
            continue
        httpx.post(
            msg['url'],
            data=msg['data']
        )


def run_consumer(consumer, topics, webhook):
    while True:
        msg = consumer.poll(0.1)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        value = msg.value().decode('utf-8')
        print('Received message: {}'.format(msg.value().decode('utf-8')))
        if webhook:
            # Push to Redis
            REDIS_CLIENT.rpush(topics, {
                'url': webhook,
                'data': {'value': json.loads(value)}
            })
    consumer.close()