"""Tests for the URLs module of the Play app."""
import pytest

from django.test import Client
from django.urls import reverse


pytestmark = pytest.mark.django_db


def test__archive__exists_at_desired_url():
    """Tests that play archive page exists at desired URL."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get('/play/archive/')

    assert response.status_code == 200


def test__archive__url_name():
    """Tests that play archive page URL name works."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get(reverse('play_archive'))

    assert response.status_code == 200


def test__play_page_detail__exists_at_desired_url(play_page):
    """Tests that play page detail exists at desired URL."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get(f'/play/{play_page.pk}/')

    assert response.status_code == 200


def test__play_page_detail__url_name(play_page):
    """Tests that play page detail URL name works."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get(reverse('play_page', kwargs={'pk': play_page.pk}))

    assert response.status_code == 200


def test__index__exists_at_desired_url():
    """Tests that play index page exists at desired URL."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get('/play/')

    assert response.status_code == 200


def test__index__url_name():
    """Tests that play index page URL name works."""
    # Create client and force user login
    client = Client()

    # Test GET request
    response = client.get(reverse('play_index'))

    assert response.status_code == 200
