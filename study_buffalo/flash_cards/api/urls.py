from django.conf.urls import include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from flash_cards import views

app_name = 'api_v1'
urlpatterns = [
    path('authentication/', include('rest_framework.urls', namespace='rest_framework')),
    path('cards/', views.CardList.as_view(), name='card_list'),
    path('cards/<uuid:id>/', views.CardDetail.as_view(), name='card_detail'),
    path('decks/', views.DeckList.as_view(), name='deck_list'),
    path('decks/<uuid:id>/', views.DeckDetail.as_view(), name='deck_detail'),
    path('tags/', views.TagList.as_view(), name='tag_list'),
    path('tags/<str:tag_name>/', views.TagDetail.as_view(), name='tag_detail'),
    path('synonyms/<str:synonym_name>/', views.SynonymDetail.as_view(), name='synonym_detail'),
    path('references/<uuid:id>/', views.ReferenceDetail.as_view(), name='reference_detail'),
    #path('part-containers/<uuid:container_uuid>/', views.PartContainerDetail.as_view(), name='part_container_detail'),
    #path('text-parts/<uuid:part_uuid>/', views.TextPartDetail.as_view(), name='text_part_detail'),
    #path(
    # 'multiple-choice-containers/<uuid:container_uuid>/',
    # views.MultipleChoiceContainerDetail.as_view(),
    # name='multiple_choice_container_detail'
    # ),
    path('', views.api_root, name='root'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
