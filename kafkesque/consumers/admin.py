from consumers.models import Consumer
from django.contrib import admin


@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    """Admin site config for Consumer model."""

    list_display = ("id", "cluster", "name", "ts_created", "ts_updated")
