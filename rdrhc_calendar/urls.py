from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^settings/$", views.calendar_settings, name="calendar_settings"),
    url(r"^$", views.calendar_index, name="calendar_index"),
]
