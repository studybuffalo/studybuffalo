"""URLs for the Play app."""
from django.urls import path

from . import views


urlpatterns = [
    path('archive/', views.Archive.as_view(), name='play_archive'),
    path('<int:pk>/', views.PlayPageDetail.as_view(), name='play_page'),
    path('', views.Index.as_view(), name='play_index'),
]
