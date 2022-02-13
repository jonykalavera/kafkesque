from django.db import models
from enum import Enum

from kafkesque.models import BaseModel
from .util import enum_as_choices


class ConsumerStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class SerializationFormat(str, Enum):
    JSON = "json"
    XML = "xml"


class Consumer(BaseModel):
    cluster = models.ForeignKey("clusters.Cluster", on_delete=models.CASCADE)
    status = models.CharField(
        choices=enum_as_choices(ConsumerStatus),
        default=ConsumerStatus.ACTIVE.value,
        max_length=100,
    )
    name = models.CharField(max_length=100)
    topics = models.CharField(max_length=300)
    serialization_format = models.CharField(
        choices=enum_as_choices(SerializationFormat),
        default=SerializationFormat.JSON.value,
        max_length=100,
    )
    webhook_url = models.URLField(blank=True, null=True)
    ts_expire = models.DateTimeField(blank=True, null=True, default=None)
    batch_size = models.SmallIntegerField(blank=True, null=True, default=None)
    # Post request triggered either when batch size is reached or when max interval time reached.
    batch_max_interval = models.IntegerField(
        blank=True, null=True, default=None
    )  # Batch max interval in seconds

    def __str__(self) -> str:
        return self.name
