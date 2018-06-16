from django.conf.urls import include
from django.urls import path, re_path
from django.views.defaults import page_not_found

from flash_cards import views

app_name = 'flash_cards'
urlpatterns = [
    # Manage all API requests
    path('api/v1/', include('flash_cards.api.urls', namespace='api_v1')),

    # Handles any URLs to the API that don't exist
    re_path('api/v1/.*', page_not_found, {'exception': Exception()}),

    # Loads the React App, which handles all further routing
    re_path('.*', views.index, name='index'),
]
