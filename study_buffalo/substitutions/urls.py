"""URLs for the Substitutions app."""
from django.urls import path

from . import views


urlpatterns = [
    path('review/delete-entry/', views.delete_pend, name='sub_delete_entry'),
    path('review/retrieve-entries/', views.retrieve_entries, name='sub_retrieve_entry'),
    path('review/verify-entry/', views.verify, name='sub_verify_entry'),
    path('review/<int:app_id>/', views.review, name='sub_review'),
    path('', views.dashboard, name='sub_dashboard'),
]
