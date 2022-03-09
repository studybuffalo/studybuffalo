"""Views for the Drug Price Calculator API."""
from django.urls import path

from api.hc_dpd import views


app_name = 'hc_dpd_api_v1'

urlpatterns = [
    # Endpoints to manage checksums
    path('checksum/', views.ChecksumList.as_view()),

    # Endpoints to modify database
    path('upload/', views.UploadHCDPDData.as_view()),
]
