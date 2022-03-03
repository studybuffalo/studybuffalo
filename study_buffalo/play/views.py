"""Views for the Play app."""
from datetime import datetime

from django.views import generic

from .models import PlayPage


class Index(generic.ListView):
    """Index view for the Play app."""
    context_object_name = 'play_page'
    template_name = 'play/index.html'

    def get_queryset(self):
        return PlayPage.objects.filter(release_date__date__lte=datetime.now()).order_by('-id').first()

class Archive(generic.ListView):
    """Archive view for the Play app."""
    model = PlayPage

    context_object_name = 'play_page_list'

class PlayPageDetail(generic.DetailView):
    """Detail view for a Play item."""
    model = PlayPage

    context_object_name = 'play_page'
