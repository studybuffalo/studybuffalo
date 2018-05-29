from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('api/v1/', include('flash_cards.api.urls'), name='api-v1'),
]
