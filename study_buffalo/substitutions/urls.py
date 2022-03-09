"""URLs for the Substitutions app."""
from django.urls import path

from . import views


urlpatterns = [
    path('review/<int:id>/', views.review, name='sub_review'),
    path('review/retrieve-entries/', views.retrieve_entries, name='retrieve_entry'),
    path('review/verify-entry/', views.verify, name='verify_entry'),
    path('review/delete-entry/', views.delete_pend, name='delete_entry'),
    path('', views.dashboard, name='dashboard'),
]
