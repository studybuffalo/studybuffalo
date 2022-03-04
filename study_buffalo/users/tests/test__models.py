"""Tests for the User models."""
import pytest


pytestmark = pytest.mark.django_db

def test__user__str__(user):
    """Tests that __str__ works as expected."""
    assert str(user) == user.username

def test__user__get_absolute_url(user):
    """Tests that get_absolute_url works as expected."""
    assert user.get_absolute_url() == '/users/{}/'.format(str(user))
