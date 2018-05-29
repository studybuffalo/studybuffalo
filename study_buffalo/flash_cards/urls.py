from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from flash_cards import views

urlpatterns = [
    path('cards/', views.Cards.as_view(), name='card-list'),
    path('decks/', views.DeckList.as_view(), name='deck-list'),
    path('decks/<uuid:deck_uuid>/', views.DeckDetail.as_view(), name='deck-detail'),
    path('tags/', views.tags, name='tag-list'),
    path('', views.api_root, name='root'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
