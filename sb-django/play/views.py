from django.shortcuts import render
from django.views import generic
from .models import PlayPage
from datetime import datetime

class Index(generic.ListView):
    queryset = PlayPage.objects.filter(release_date__date__lte=datetime.now()).order_by("-id")[0]
    context_object_name = "play_page"
    template_name = "play/index.html"

class Archive(generic.ListView):
    model = PlayPage

    context_object_name = "play_page_list"

class PlayPageDetail(generic.DetailView):
    model = PlayPage
    
    context_object_name = "play_page"