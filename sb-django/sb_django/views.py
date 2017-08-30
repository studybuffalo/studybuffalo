from django.views import generic
from django.shortcuts import render
from carousel.models import CarouselSlide

class Index(generic.ListView):
    model = CarouselSlide

    context_object_name = "slides"
    template_name = "index.html"

def tools_index(request):
    """View for the tool page"""
    return render(
        request,
        "tools_index.html",
        context={},
    )

def alberta_adaptations_index(request):
    """View for the alberta adaptations page"""
    return render(
        request,
        "alberta_adaptations_index.html",
        context={},
    )

def design_index(request):
    """View for the design page"""
    return render(
        request,
        "design_index.html",
        context={},
    )