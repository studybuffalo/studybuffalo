from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^review/(?P<id>\d+)$", views.review, name="sub_review"),
    url(r"^review/retrieve-entries/$", views.retrieve_entries, name="retrieve_entry"),
    url(r"^review/verify-entry/$", views.verify, name="verify_entry"),
    url(r"^review/delete-entry/$", views.delete_pend, name="delete_entry"),
    url(r"^$", views.dashboard, name="dashboard"),
]
