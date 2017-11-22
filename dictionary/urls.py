from django.conf.urls import url

from .views import review, index, retrieve_entries

urlpatterns = [
    url(r"^review/$", review, name="dictionary_review"),
    url(
        r"^review/retrieve-entries/$", 
        retrieve_entries, 
        name="dictionary_retrieve_entry"
    ),
    url(r"^$", index, name="dictionary_index"),
]
