"""Tests for the Views module of the Study app."""
import pytest

from django.test import Client, RequestFactory
from django.urls import reverse

from study import views


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
    response = client.get(reverse('study_index'))

    # Test for template
    assert 'study/index.html' in [t.name for t in response.templates]


def test__index__context_name():
    """Confirms index view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('study_index'))

    # Test for context_object_name
    assert 'guide_list' in response.context


def test__guide_detail__200_resonse(study_guide):
    """Confirms guide detail view returns 200 response."""
    # Create request, view, and response
    request = RequestFactory()
    request.method = 'GET'
    response = views.GuideDetail.as_view()(request, pk=study_guide.pk)

    # Confirm status code
    assert response.status_code == 200


def test__guide_detail__template(study_guide):
    """Confirms guide detail view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('study_guide_page', kwargs={'pk': study_guide.pk}))

    # Test for template
    assert 'study/guide_detail.html' in [t.name for t in response.templates]


def test__guide_detail__context_name(study_guide):
    """Confirms guide detail view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('study_guide_page', kwargs={'pk': study_guide.pk}))

    # Test for context_object_name
    assert 'guide_page' in response.context
