import logging
from typing import List, Optional

from channels.layers import get_channel_layer
from ninja import Router, Schema
from pydantic import HttpUrl
from .models import WebhookConfig

channel_layer = get_channel_layer()
router = Router()
logger = logging.getLogger(__name__)


class ConsumerRequest(Schema):
    name: str
    topics: List[str]
    format: str = "json"
    auto_offset_reset: str = "earliest"
    webhook_url: Optional[HttpUrl]
    ts_expire: Optional[str] = None
    batch_size: Optional[int] = 1
    max_batch_interval: Optional[int] = None


@router.post("/")
async def create_consumer(request, consumer: ConsumerRequest):
    await channel_layer.send(
        "kafka-consume",
        {
            "type": "kafka.consume",
            "topics": consumer.topics,
            "name": consumer.name,
            "format": consumer.format,
            "auto.offset.reset": consumer.auto_offset_reset,
            "webhook": consumer.webhook_url,
        },
    )

    # Check if exactly the same config already exists
    _, created = WebhookConfig.objects.update_or_create(
        url=consumer.webhook_url,
        topics=consumer.topics,
        defaults={
            'serialization_format': consumer.format,
            'ts_expire': consumer.ts_expire,
            'batch_size': consumer.batch_size,
            'batch_max_interval': consumer.max_batch_interval
        }
    )
    if created:
        logger.info('Created new webhook for URL: %s, topics: %s', consumer.webhook_url, str(consumer.topics))
    else:
        logger.info('Updated webhook for URL: %s, topic: %s', consumer.webhook_url, str(consumer.topics))

