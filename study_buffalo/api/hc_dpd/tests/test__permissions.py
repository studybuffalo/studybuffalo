"""Tests for the HC DPD API permissions."""
import pytest

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from api.hc_dpd.tests import utils
from study_buffalo.api.hc_dpd import permissions


pytestmark = pytest.mark.django_db


def test__has_dpd_view_access__anonymous_user():
    """Confirms anonymous users fail permission check."""
    permission = permissions.HasDPDViewAccess()
    request = RequestFactory()
    request.user = AnonymousUser()

    assert permission.has_permission(request, None) is False


def test__has_dpd_view_access__user_without_permission(user):
    """Confirms user without permission fail permission check."""
    permission = permissions.HasDPDViewAccess()
    request = RequestFactory()
    request.user = user

    assert permission.has_permission(request, None) is False


def test__has_dpd_view_access__user_with_permission(user):
    """Confirms user with permission passes permission check."""
    # Add permission to user
    utils.add_api_view_permission(user)

    permission = permissions.HasDPDViewAccess()
    request = RequestFactory()
    request.user = user

    assert permission.has_permission(request, None) is True


def test__has_dpd_edit_access__anonymous_user():
    """Confirms anonymous users fail permission check."""
    permission = permissions.HasDPDEditAccess()
    request = RequestFactory()
    request.user = AnonymousUser()

    assert permission.has_permission(request, None) is False


def test__has_dpd_edit_access__user_without_permission(user):
    """Confirms user without permission fail permission check."""
    permission = permissions.HasDPDEditAccess()
    request = RequestFactory()
    request.user = user

    assert permission.has_permission(request, None) is False


def test__has_dpd_edit_access__user_with_permission(user):
    """Confirms user with permission passes permission check."""
    # Add permission to user
    utils.add_api_edit_permission(user)

    permission = permissions.HasDPDEditAccess()
    request = RequestFactory()
    request.user = user

    assert permission.has_permission(request, None) is True
