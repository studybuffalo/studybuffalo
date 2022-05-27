"""Views for the Drug Price Calculator API."""
from django.urls import path

from api.hc_dpd import views


app_name = 'hc_dpd_v1'

urlpatterns = [
    # Endpoints to manage checksums
    path('checksum/', views.ChecksumList.as_view(), name='checksum_list'),

    # Endpoints to modify database
    path('upload/', views.UploadHCDPDData.as_view(), name='upload_hc_dpd_data'),
]
