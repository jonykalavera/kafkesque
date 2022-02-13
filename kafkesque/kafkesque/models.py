import uuid
from django.db import models


class BaseModel(models.Model):
    """Base model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ts_created = models.DateTimeField(auto_now_add=True)
    ts_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
