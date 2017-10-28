from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^settings/$", views.calendar_settings, name="calendar_settings"),
    url(r"^shifts/$", views.ShiftCodeList.as_view(), name="calendar_code_list"),
    url(r"^shifts/(?P<code>\w+)$", views.calendar_code_edit, name="calendar_code_edit"),
    url(r"^shifts/add/$", views.calendar_code_add, name="calendar_code_add"),
    url(r"^shifts/delete/(?P<code>\w+)$", views.calendar_code_delete, name="calendar_code_delete"),
    url(r"^missing-codes/$", views.MissingShiftCodeList.as_view(), name="calendar_missing_code_list"),
    url(r"^missing-codes/add/(?P<id>\d+)$", views.missing_code_add, name="calendar_missing_code_add"),
    url(r"^missing-codes/delete/(?P<id>\d+)$", views.missing_code_delete, name="calendar_missing_code_delete"),
    url(r"^$", views.calendar_index, name="calendar_index"),
]
