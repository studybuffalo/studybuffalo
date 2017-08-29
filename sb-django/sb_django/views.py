from django.views import generic
from django.shortcuts import render
from carousel.models import CarouselSlide

class Index(generic.ListView):
    model = CarouselSlide

    context_object_name = "slides"
    template_name = "index.html"

def design_index(request):
    """View for the design page"""
    return render(
        request,
        "design_index.html",
        context={},
    )