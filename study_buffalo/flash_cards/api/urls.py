from django.conf.urls import include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from flash_cards import views

urlpatterns = [
    path('authentication/', include('rest_framework.urls')),
    path('cards/', views.Cards.as_view(), name='card_list'),
    path('decks/', views.DeckList.as_view(), name='deck_list'),
    path('decks/<uuid:deck_uuid>/', views.DeckDetail.as_view(), name='deck_detail'),
    path('tags/', views.tags, name='tag_list'),
    path('', views.api_root, name='root'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
