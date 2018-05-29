from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('api/', include('flash_cards.api.urls')),
]
