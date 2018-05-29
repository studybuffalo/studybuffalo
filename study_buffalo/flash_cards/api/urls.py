from django.conf.urls import include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from flash_cards import views

urlpatterns = [
    path('authentication/', include('rest_framework.urls')),
    path('v1/cards/', views.Cards.as_view(), name='card-list'),
    path('v1/decks/', views.DeckList.as_view(), name='deck-list'),
    path('v1/decks/<uuid:deck_uuid>/', views.DeckDetail.as_view(), name='deck-detail'),
    path('v1/tags/', views.tags, name='tag-list'),
    path('v1/', views.api_root, name='root'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
