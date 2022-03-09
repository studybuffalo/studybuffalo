"""URLs for the Dictionary application."""
from django.urls import path

from .views import (
    review, index, retrieve_entries, add_new_word, delete_pending_word,
    retrieve_select_data
)


urlpatterns = [
    path('review/', review, name='dictionary_review'),
    path('review/retrieve-entries/', retrieve_entries, name='dictionary_retrieve_entry'),
    path('review/add-new-word/', add_new_word),
    path('review/delete-pending-word/', delete_pending_word),
    path('review/retrieve-select-data/', retrieve_select_data),
    path('', index, name='dictionary_index'),
]
