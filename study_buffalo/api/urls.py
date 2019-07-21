"""URLs for the Study Buffalo APIs."""
from django.conf.urls import include
from django.urls import path


app_name = 'api'

urlpatterns = [
    path('authentication/', include('rest_framework.urls')),
    path('rdrhc-calendar/v1/', include('api.rdrhc_calendar.urls', namespace='rdrhc_calendar_v1')),
    path('drug-price-calculator/v1/', include('api.drug_price_calculator.urls')),
]
