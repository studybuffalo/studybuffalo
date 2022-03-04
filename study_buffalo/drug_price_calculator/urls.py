"""URLs for the Drug Price Calculator application."""
from django.urls import path
from . import views


urlpatterns = [
    # Frontend endpoints
    path('coverage-criteria/<int:price_id>/', views.prices_coverage_criteria),
    path('', views.index, name='drug_price_calculator_index'),
]
