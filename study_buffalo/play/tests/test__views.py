"""Tests for the Views module of the Play app."""
from datetime import timedelta

import pytest

from django.test import Client, RequestFactory
from django.urls import reverse
from django.utils import timezone

from play import models, views


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


def test__index__get_queryset(play_page):
    """Confirms index view returns expected template."""
    # Save FK references
    category = play_page.category

    # Clear existing pages
    models.PlayPage.objects.all().delete()

    # Create test models
    now = timezone.now()
    last_year = now - timedelta(days=365)
    last_month = now - timedelta(days=30)
    next_year = now + timedelta(days=365)
    models.PlayPage.objects.create(
        title='Page 1',
        date=now,
        category=category,
        release_date=last_year,
    )
    page_2 = models.PlayPage.objects.create(
        title='Page 2',
        date=now,
        category=category,
        release_date=last_month,
    )
    page_3 = models.PlayPage.objects.create(
        title='Page 2',
        date=now,
        category=category,
        release_date=next_year,
    )

    # Create request, view, and queryset
    request = RequestFactory()
    view = views.Index()
    view.setup(request)
    queryset = view.get_queryset()

    # Confirm only 1 instance returned
    assert isinstance(queryset, models.PlayPage)

    # Confirm that page_3 was filtered out
    assert queryset.pk != page_3.pk

    # Confirm that page_2 was the returned instance
    assert queryset.pk == page_2.pk


def test__index__template():
    """Confirms index view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('play_index'))

    # Test for template
    assert 'play/index.html' in [t.name for t in response.templates]


def test__index__context_name():
    """Confirms index view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('play_index'))

    # Test for context_object_name
    assert 'play_page' in response.context


def test__archive__200_resonse():
    """Confirms archive view returns 200 response."""
    # Create request, view, and response
    request = RequestFactory()
    view = views.Archive()
    view.setup(request)
    response = view.get(request)

    # Confirm status code
    assert response.status_code == 200


def test__archive__template():
    """Confirms archive view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('play_archive'))

    # Test for template
    assert 'play/playpage_list.html' in [t.name for t in response.templates]


def test__archive__context_name():
    """Confirms archive view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('play_archive'))

    # Test for context_object_name
    assert 'play_page_list' in response.context


def test__play_page_detail__200_resonse(play_page):
    """Confirms play page detail view returns 200 response."""
    # Create request, view, and response
    request = RequestFactory()
    request.method = 'GET'
    response = views.PlayPageDetail.as_view()(request, pk=play_page.pk)

    # Confirm status code
    assert response.status_code == 200


def test__play_page_detail__template(play_page):
    """Confirms play page detail view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('play_page', kwargs={'pk': play_page.pk}))

    # Test for template
    assert 'play/playpage_detail.html' in [t.name for t in response.templates]


def test__play_page_detail__context_name(play_page):
    """Confirms play page detail view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('play_page', kwargs={'pk': play_page.pk}))

    # Test for context_object_name
    assert 'play_page' in response.context
