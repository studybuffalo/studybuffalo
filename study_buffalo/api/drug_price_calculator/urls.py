"""Views for the Drug Price Calculator API."""
from django.urls import path

from api.drug_price_calculator import views


app_name = 'drug_price_calculator_v1'

urlpatterns = [
    # Endpoints to modify database
    path('<str:din>/upload/', views.UploadiDBLData.as_view()),
]
