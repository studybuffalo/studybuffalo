from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from flash_cards import views

urlpatterns = [
    path('tag', views.TagList.as_view(), name='tag-list'),
    path('tag/<int:pk>/', views.TagDetail.as_view(), name='tag-detail'),
    path('synonym', views.SynonymList.as_view(), name='synonym-list'),
    path('synonym/<int:pk>/', views.SynonymDetail.as_view(), name='synonym-detail'),
    path('', views.api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)
