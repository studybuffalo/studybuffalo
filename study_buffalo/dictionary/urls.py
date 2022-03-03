"""URLs for the Dictionary application."""
from django.conf.urls import url

from .views import (
    review, index, retrieve_entries, add_new_word, delete_pending_word,
    retrieve_select_data
)


urlpatterns = [
    url(r'^review/$', review, name='dictionary_review'),
    url(
        r'^review/retrieve-entries/$',
        retrieve_entries,
        name='dictionary_retrieve_entry'
    ),
    url(r'^review/add-new-word', add_new_word),
    url(r'^review/delete-pending-word', delete_pending_word),
    url(r'^review/retrieve-select-data', retrieve_select_data),
    url(r'^$', index, name='dictionary_index'),
]
