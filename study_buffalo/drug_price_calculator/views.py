"""Views for the Drug Price Calculator."""
from django.shortcuts import render, get_object_or_404

from . import models


def index(request):
    """View for the main drug price calculator page"""
    return render(
        request,
        "drug_price_calculator/index.html",
        context={},
    )

def prices_coverage_criteria(request, price_id):
    """View for the coverage criteria of a price file."""
    price = get_object_or_404(models.Price, id=price_id)

    return render(
        request,
        'drug_price_calculator/prices_coverage_criteria.html',
        context={
            'coverage_criteria': price.coverage_criteria.all(),
        },
    )
