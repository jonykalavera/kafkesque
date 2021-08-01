from typing import List, Optional

from channels.layers import get_channel_layer
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ninja import Router, Schema
from pydantic import HttpUrl

channel_layer = get_channel_layer()
router = Router()


class ConsumerRequest(Schema):
    name: str
    topics: List[str]
    format: str = "json"
    auto_offset_reset: str = "earliest"
    webhook_url: Optional[HttpUrl]


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
