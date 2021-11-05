"""kafkesque URL Configuration
"""
import re
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from consumers.views import echo
from django.views.static import serve
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("echo/", echo),
    # serve static files since they are only used from admin
    re_path(
        r"^%s(?P<path>.*)$" % re.escape(settings.STATIC_URL.lstrip("/")),
        serve,
        kwargs={
            "document_root": settings.STATIC_ROOT,
            "show_indexes": False,
        },
    ),
]
