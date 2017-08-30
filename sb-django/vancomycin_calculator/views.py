from django.shortcuts import render

def index(request):
    """View for the main vancomycin calculator page"""
    return render(
        request,
        "vancomycin_calculator/index.html",
        context={},
    )