"""Tests for the URLs module of the Read app."""
import pytest

from django.test import Client
from django.urls import reverse


pytestmark = pytest.mark.django_db


def test__read_publication_detail__exists_at_desired_url(read_publication):
    """Tests that read page detail exists at desired URL."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get(f'/read/{read_publication.pk}/')

    assert response.status_code == 200


def test__read_publication_detail__url_name(read_publication):
    """Tests that read page detail URL name works."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get(reverse('pub_page', kwargs={'pk': read_publication.pk}))

    assert response.status_code == 200


def test__index__exists_at_desired_url():
    """Tests that play index page exists at desired URL."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get('/read/')

    assert response.status_code == 200


def test__index__url_name():
    """Tests that play index page URL name works."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get(reverse('pub_index'))

    assert response.status_code == 200
