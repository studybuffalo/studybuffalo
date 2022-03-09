"""URLs for the Study app."""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='study_index'),
    path('<int:pk>/', views.GuideDetail.as_view(), name='study_guide_page'),
]
