from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^settings/$", views.calendar_settings, name="calendar_settings"),
    url(r"^shifts/$", views.ShiftCodeList.as_view(), name="calendar_shift_code_list"),
    url(r"^shifts/(?P<code>\w*)$", views.calendar_shift_code, name="calendar_shift_code"),
    url(r"^$", views.calendar_index, name="calendar_index"),
]
