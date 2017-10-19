from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^apps/$", views.AppList.as_view(), name="app_list"),
    url(r"^apps/add", views.app_add, name="app_add"),
    url(r"^$", views.LogEntries.as_view(), name="log_entries"),
]