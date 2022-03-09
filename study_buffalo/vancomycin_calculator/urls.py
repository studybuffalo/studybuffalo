"""URLs for the Vancomycin Calculator app."""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='vancomycin_calculator_index'),
]
