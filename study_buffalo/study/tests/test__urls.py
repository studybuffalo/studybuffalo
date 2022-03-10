"""Tests for the URLs module of the Study app."""
import pytest

from django.test import Client
from django.urls import reverse


pytestmark = pytest.mark.django_db


def test__study_guide_page__exists_at_desired_url(study_guide):
    """Tests that study guide page detail exists at desired URL."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get(f'/study/{study_guide.pk}/')

    assert response.status_code == 200


def test__study_guide_page__url_name(study_guide):
    """Tests that study guide page detail URL name works."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get(reverse('study_guide_page', kwargs={'pk': study_guide.pk}))

    assert response.status_code == 200


def test__index__exists_at_desired_url():
    """Tests that play index page exists at desired URL."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get('/study/')

    assert response.status_code == 200


def test__index__url_name():
    """Tests that play index page URL name works."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get(reverse('study_index'))

    assert response.status_code == 200
