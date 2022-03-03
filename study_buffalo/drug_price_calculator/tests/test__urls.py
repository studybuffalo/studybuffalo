"""Tests for Drug Price Calculator Views."""
import pytest

from django.test import Client
from django.urls import reverse

from drug_price_calculator.models import Drug, Price, CoverageCriteria


pytestmark = pytest.mark.django_db

def test__index__exists_at_desired_url():
    """Tests that index page exists at desired URL."""
    client = Client()
    response = client.get('/tools/drug-price-calculator/')

    assert response.status_code == 200

def test__index__url_name():
    """Tests that index page URL name works."""
    client = Client()
    response = client.get(reverse('drug_price_calculator_index'))

    assert response.status_code == 200

def test__coverage_criteria__exists_at_desired_url():
    """Tests that index page exists at desired URL."""
    # Create CoverageCriteria instance for URL test
    drug = Drug.objects.create(din='12345678')
    price = Price.objects.create(drug=drug, abc_id=1)
    CoverageCriteria.objects.create(price=price, criteria='a')

    client = Client()
    response = client.get(
        f'/tools/drug-price-calculator/coverage-criteria/{price.id}/'
    )

    assert response.status_code == 200
