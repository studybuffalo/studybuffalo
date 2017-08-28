from django.views import generic
from carousel.models import CarouselSlide

class Index(generic.ListView):
    model = CarouselSlide

    context_object_name = "slides"
    template_name = "index.html"