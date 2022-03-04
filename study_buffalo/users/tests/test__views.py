"""Tests for the User Views."""
import pytest

from django.test.client import RequestFactory

from users.views import UserRedirectView, UserUpdateView


pytestmark = pytest.mark.django_db


def test__user_redirect_view__get_redirect_url(user):
    """Tests the get_redirect_url method of UserRedirectView."""
    # Create view and request for testing
    request = RequestFactory()
    request.user = user
    view = UserRedirectView()
    view.request = request

    assert view.get_redirect_url() == f'/users/{user.username}/'


def test__user_update_view__get_success_url(user):
    """Tests the get_success_url method of UserUpdateView."""
    # Create view and request for testing
    request = RequestFactory()
    request.user = user
    view = UserUpdateView()
    view.request = request

    assert view.get_success_url() == f'/users/{user.username}/'


def test__user_update_view__get_object(user):
    """Tests the get_object method of UserUpdateView."""
    # Create view and request for testing
    request = RequestFactory()
    request.user = user
    view = UserUpdateView()
    view.request = request

    assert view.get_object() == user
