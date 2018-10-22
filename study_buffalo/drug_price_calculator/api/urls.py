from django.conf.urls import include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from drug_price_calculator.api import views

app_name = 'api_v1'
urlpatterns = [
    path('authentication/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)

"""API Endpoint Planner

- Currently removes data from database - can we keep a historical record?
  - Simple history?
- Uploads:
  - ATC
  - Coverage
  - Extra data
  - Price data
  - PTC
  - Special authorization


OTHER
  - Will need an API as well for the substitution application
  - Need to send data for substitution screening
    - BSRF
    - Generic
    - Manufacturer
    - PTC
    -
  - Need to request list of data for substitutions

"""
