from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.calendar_index, name="calendar_index"),
]
