from django.db import models
from enum import Enum
from .util import enum_as_choices


class WebhookStatus(Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class SerializationFormat(Enum):
    JSON = 'json'
    XML = 'xml'


# TODO: replace with Pydantic model?
class WebhookConfig(models.Model):

    url = models.URLField()
    topic = models.CharField(max_length=200)
    serialization_format = models.CharField(choices=enum_as_choices(SerializationFormat), default=SerializationFormat,
                                            max_length=100)
    status = models.CharField(choices=enum_as_choices(WebhookStatus), default=WebhookStatus.ACTIVE, max_length=100)
    ts_expire = models.DateTimeField(blank=True, null=True, default=None)
    batch_size = models.SmallIntegerField(blank=True, null=True, default=None)
    # Post request triggered either when batch size is reached or when max interval time reached.
    batch_max_interval = models.IntegerField(blank=True, null=True, default=None) # Batch max interval in seconds
