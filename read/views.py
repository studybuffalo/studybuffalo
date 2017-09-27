from django.shortcuts import render
from django.views import generic
from .models import Publication

class Index(generic.ListView):
    model = Publication
    context_object_name = "pub_list"
    template_name = "read/index.html"

class PublicationDetail(generic.DetailView):
    model = Publication

    context_object_name = "publication_page"