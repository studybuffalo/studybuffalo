"""Tests for the Views module of the Read app."""
import pytest

from django.test import Client, RequestFactory
from django.urls import reverse

from read import views


pytestmark = pytest.mark.django_db


def test__index__200_resonse():
    """Confirms index view returns 200 response."""
    # Create request, view, and response
    request = RequestFactory()
    view = views.Index()
    view.setup(request)
    response = view.get(request)

    # Confirm status code
    assert response.status_code == 200


def test__index__template():
    """Confirms index view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('pub_index'))

    # Test for template
    assert 'read/index.html' in [t.name for t in response.templates]


def test__index__context_name():
    """Confirms index view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('pub_index'))

    # Test for context_object_name
    assert 'pub_list' in response.context


def test__publication_detail__200_resonse(read_publication):
    """Confirms publication detail view returns 200 response."""
    # Create request, view, and response
    request = RequestFactory()
    request.method = 'GET'
    response = views.PublicationDetail.as_view()(request, pk=read_publication.pk)

    # Confirm status code
    assert response.status_code == 200


def test__publication_detail__template(read_publication):
    """Confirms publication detail view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('pub_page', kwargs={'pk': read_publication.pk}))

    # Test for template
    assert 'read/publication_detail.html' in [t.name for t in response.templates]


def test__publication_detail__context_name(read_publication):
    """Confirms publication detail view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('pub_page', kwargs={'pk': read_publication.pk}))

    # Test for context_object_name
    assert 'publication_page' in response.context
