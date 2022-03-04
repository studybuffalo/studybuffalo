"""Views for the Study app."""
from django.views import generic
from .models import Guide


class Index(generic.ListView):
    """Index view for the Study app."""
    model = Guide
    context_object_name = 'guide_list'
    template_name = 'study/index.html'


class GuideDetail(generic.DetailView):
    """Detail view for a Guide."""
    model = Guide

    context_object_name = 'guide_page'
