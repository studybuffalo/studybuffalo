"""URLs for the Read app."""
from django.urls import path

from . import views


urlpatterns = [
    path('<int:pk>/', views.PublicationDetail.as_view(), name='pub_page'),
    path('', views.Index.as_view(), name='pub_index'),
]
