from django.conf.urls import include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from flash_cards import views

app_name='flash_cards'
urlpatterns = [
    path('api/v1/', include('flash_cards.api.urls', namespace='api_v1')),
]
