"""kafkesque URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
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
