from django.conf.urls import include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from flash_cards import views

app_name = 'api_v1'
urlpatterns = [
    path('authentication/', include('rest_framework.urls')),
    path('cards/', views.Cards.as_view(), name='card_list'),
    path('decks/', views.DeckList.as_view(), name='deck_list'),
    path('decks/<uuid:deck_uuid>/', views.DeckDetail.as_view(), name='deck-detail'),
    path('tags/', views.TagList.as_view(), name='tag_list'),
    path('tags/<uuid:tag_uuid>/', views.TagDetail.as_view(), name='tag_detail'),
    path('synonyms/<uuid:synonym_uuid>', views.SynonymDetail.as_view(), name='synonym_detail'),
    path('references/<uuid:reference_uuid', views.ReferenceDetail.as_view(), name='reference_detail'),
    path('', views.api_root, name='root'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
