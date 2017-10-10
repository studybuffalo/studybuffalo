from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^how-to$", views.calendar_index, name="calendar_index"),
]
