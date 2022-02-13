from django.contrib import admin
from clusters.models import Cluster


@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    """Admin config for Cluster model."""

    list_display = ("id", "name", "ts_created", "ts_updated")
