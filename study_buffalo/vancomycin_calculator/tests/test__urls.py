"""Tests for the URLs module of the Vancomycin Calculator app."""
import pytest

from django.test import Client
from django.urls import reverse


pytestmark = pytest.mark.django_db


def test__index__exists_at_desired_url():
    """Tests that play index page exists at desired URL."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get('/tools/vancomycin-calculator/')

    assert response.status_code == 200


def test__index__url_name():
    """Tests that play index page URL name works."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get(reverse('vancomycin_calculator_index'))

    assert response.status_code == 200
