from django.db import models
from django.conf import settings

from kafkesque.models import BaseModel


DEFAULT_CLUSTER_CONFIG = {
    "bootstrap.servers": f"{settings.KAFKA_BOOTSTRAP_SERVERS}",
    "group.id": f"kafkesque",
    "auto.offset.reset": "latest",
}


def default_config():
    return DEFAULT_CLUSTER_CONFIG.copy()


# Create your models here.
class Cluster(BaseModel):
    name = models.CharField(max_length=100)
    config = models.JSONField(default=default_config)

    def __str__(self) -> str:
        return self.name
