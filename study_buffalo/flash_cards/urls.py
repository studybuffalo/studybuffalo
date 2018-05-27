from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from flash_cards import views

urlpatterns = [
    path('cards/', views.cards, name='card-list'),
    path('decks/', views.decks, name='deck-list'),
    path('tags/', views.tags, name='tag-list'),
    path('', views.api_root, name='root'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
