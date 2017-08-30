from django.shortcuts import render

def index(request):
    """View for the main drug price calculator page"""
    return render(
        request,
        "drug_price_calculator/index.html",
        context={},
    )