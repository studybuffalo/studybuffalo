from django.conf.urls import include
from django.urls import path

app_name = 'flash_cards'
urlpatterns = [
    path('api/v1/', include('flash_cards.api.urls', namespace='api_v1')),
]
