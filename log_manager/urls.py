from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^apps/$", views.AppList.as_view(), name="app_list"),
    url(r"^apps/add", views.app_add, name="app_add"),
    url(r"^apps/(?P<id>\d+)$", views.app_edit, name="app_edit"),
    url(r"^apps/delete/(?P<id>\d+)$", views.app_delete, name="app_delete"),
    url(r"^$", views.LogEntries.as_view(), name="log_entries"),
]