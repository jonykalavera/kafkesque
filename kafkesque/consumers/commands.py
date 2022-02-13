from asyncio import constants
import logging
from typing import TYPE_CHECKING

from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from clusters.models import Cluster
from clusters.schemas import ClusterSchema
from consumers.models import Consumer
from consumers.schemas import CreateConsumerSchema, StartConsumerSchema

if TYPE_CHECKING:
    from django.db.models import QuerySet

channel_layer = get_channel_layer()
logger = logging.getLogger(__name__)


def create_consumer(cmd: CreateConsumerSchema) -> Consumer:
    data = cmd.dict()
    try:
        data["cluster"] = Cluster.objects.get(id=cmd.cluster)
    except Cluster.DoesNotExist:
        raise ValueError("invalid cluster")
    instance = Consumer.objects.create(**data)
    logger.info("Created new consumer for topics: %s", cmd.topics)
    return instance


def get_consumers() -> "QuerySet":
    return Consumer.objects.all()


def get_consumer(consumer_id):

    return Consumer.objects.prefetch_related("cluster").get(id=consumer_id)


async def start_consumer(consumer_id):
    consumer = await database_sync_to_async(get_consumer)(consumer_id)
    cmd = await database_sync_to_async(StartConsumerSchema.from_django)(consumer)
    kwargs = cmd.dict()
    kwargs["cluster"] = (
        await database_sync_to_async(ClusterSchema.from_django)(consumer.cluster)
    ).dict(exclude={"id", "ts_created", "ts_updated", "consumer"})
    await channel_layer.send(
        "kafka-consumer",
        {"type": "kafka.start.consumer", **kwargs},
    )
