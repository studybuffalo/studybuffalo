"""Tests for the Views module of the Vancomycin Calculator app."""
import pytest

from django.test import Client
from django.urls import reverse


pytestmark = pytest.mark.django_db


def test__index__template():
    """Confirms index view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('vancomycin_calculator_index'))

    # Test for template
    assert 'vancomycin_calculator/index.html' in [t.name for t in response.templates]
