from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^apps/$", views.AppList.as_view(), name="app_list"),
    url(r"^apps/add", views.app_add, name="app_add"),
    url(r"^apps/(?P<id>\d+)$", views.app_edit, name="app_edit"),
    url(r"^apps/delete/(?P<id>\d+)$", views.app_delete, name="app_delete"),
    url(r"^update-entries/$", views.update_entries, name="update_entries"),
    url(r"^all/$", views.AllLogEntries.as_view(), name="log_entries_all"),
    url(r"^$", views.log_entries, name="log_entries"),
]