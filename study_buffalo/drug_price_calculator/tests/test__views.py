"""Tests for Drug Price Calculator Views."""
import pytest

from django.test import Client
from django.urls import reverse

from drug_price_calculator.models import Drug, Price, CoverageCriteria


pytestmark = pytest.mark.django_db


def test__index__template():
    """Tests for proper index template."""
    client = Client()
    response = client.get(reverse('drug_price_calculator_index'))

    assert (
        'drug_price_calculator/index.html' in [t.name for t in response.templates]
    )

def test__prices_coverage_criteria__template():
    """Tests for proper price_coverage_criteria template."""
    # Create CoverageCriteria instance for test
    drug = Drug.objects.create(din='12345678')
    price = Price.objects.create(drug=drug, abc_id=1)
    CoverageCriteria.objects.create(price=price, criteria='a')

    client = Client()
    response = client.get(
        f'/tools/drug-price-calculator/coverage-criteria/{price.id}/'
    )

    assert (
        'drug_price_calculator/prices_coverage_criteria.html' in [t.name for t in response.templates]
    )

def test__prices_coverage_criteria__404_handling():
    """Tests price_coverage_criteria returns 404 if invalid price ID."""
    client = Client()
    response = client.get(
        '/tools/drug-price-calculator/coverage-criteria/0/'
    )

    assert response.status_code == 404

def test__prices_coverage_criteria__context__criteria():
    """Tests price_coverage_criteria criteria in context."""
    # Create CoverageCriteria instance for test
    drug = Drug.objects.create(din='12345678')
    price = Price.objects.create(drug=drug, abc_id=1)
    criteria = CoverageCriteria.objects.create(price=price, criteria='a')

    client = Client()
    response = client.get(
        f'/tools/drug-price-calculator/coverage-criteria/{price.id}/'
    )

    assert 'coverage_criteria' in response.context
    assert criteria in response.context['coverage_criteria']
