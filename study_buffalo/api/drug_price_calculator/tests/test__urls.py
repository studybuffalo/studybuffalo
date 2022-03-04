"""Tests for Drug Price Calculator API URLs."""
import pytest

from rest_framework.test import APIClient

from .utils import create_token


pytestmark = pytest.mark.django_db


def test__upload__exists_at_desired_url(user):
    """Tests that iDBL data upload view exists at desired URL."""
    # Create a token for the user
    token = create_token(user)

    # Get DIN for URL
    din = '12345678'

    # Authenticate and make request
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    response = client.post(
        f'/api/drug-price-calculator/v1/{din}/upload/',
        data={'din': din, 'abc_id': 1}
    )

    assert response.status_code == 201


def test__drugs_list__exists_at_desired_url():
    """Tests that the DrugList view exists at desired URL."""
    # Make request
    client = APIClient()
    response = client.get('/api/drug-price-calculator/v1/drugs/')

    assert response.status_code == 200


def test__drug_price_list__exists_at_desired_url():
    """Tests that the DrugPriceList view exists at desired URL."""
    # Make request
    client = APIClient()
    response = client.get('/api/drug-price-calculator/v1/drugs/prices/?ids=1')

    assert response.status_code == 200
