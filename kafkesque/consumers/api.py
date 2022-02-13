""" Consumers api.
"""
import logging
from typing import List

from ninja import Router
from ninja.errors import ValidationError

from consumers import commands
from consumers.schemas import ConsumerSchema, CreateConsumerSchema


router = Router()
logger = logging.getLogger(__name__)


@router.post("/", response={201: ConsumerSchema})
def create_consumer(_request, cmd: CreateConsumerSchema):
    """Create consumer."""
    try:
        instance = commands.create_consumer(cmd)
    except ValueError as err:
        raise ValidationError(err)
    return ConsumerSchema.from_django(instance)


@router.get("/", response={200: List[ConsumerSchema]})
def get_consumers(request) -> List[ConsumerSchema]:
    """Get consumers"""
    consumers = commands.get_consumers()
    return [ConsumerSchema.from_django(o) for o in consumers]


@router.post("/{consumer_id}/start")
async def start_consumer(_request, consumer_id):
    await commands.start_consumer(consumer_id)
