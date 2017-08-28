"""
Definition of urls for sb_django.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

from django.conf.urls import include
from django.contrib import admin
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^play/", include("play.urls")),
    url(r"^$", views.index, name="index"),
]