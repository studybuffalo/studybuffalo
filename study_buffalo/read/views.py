"""Views for the Read app."""
from django.views import generic
from .models import Publication

class Index(generic.ListView):
    """Index page view for the Read app."""
    model = Publication
    context_object_name = 'pub_list'
    template_name = 'read/index.html'

class PublicationDetail(generic.DetailView):
    """Detail view for a Publication."""
    model = Publication

    context_object_name = 'publication_page'
