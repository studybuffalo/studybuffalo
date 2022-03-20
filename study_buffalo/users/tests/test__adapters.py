"""Tests for the User app's adapters module."""
from unittest.mock import patch

from users import adapters


@patch('users.adapters.settings', create=True)
def test__account_adaptor__is_open_for_signup__with_settings(settings):
    """Tests is_open_for_signup when setting value set."""
    # Set setting's value to False for testing
    settings.ACCOUNT_ALLOW_REGISTRATION = False

    # Test method response
    adapter = adapters.AccountAdapter()

    assert adapter.is_open_for_signup(None) is False


@patch('users.adapters.settings', object)
def test__account_adaptor__is_open_for_signup__without_settings():
    """Tests is_open_for_signup when setting value is not set."""
    # Test method response
    adapter = adapters.AccountAdapter()

    assert adapter.is_open_for_signup(None) is True


@patch('users.adapters.settings', create=True)
def test__social_account_adaptor__is_open_for_signup__with_settings(settings):
    """Tests is_open_for_signup when setting value set."""
    # Set setting's value to False for testing
    settings.ACCOUNT_ALLOW_REGISTRATION = False

    # Test method response
    adapter = adapters.SocialAccountAdapter()

    assert adapter.is_open_for_signup(None, None) is False


@patch('users.adapters.settings', object)
def test__social_account_adaptor__is_open_for_signup__without_settings():
    """Tests is_open_for_signup when setting value is not set."""
    # Test method response
    adapter = adapters.SocialAccountAdapter()

    assert adapter.is_open_for_signup(None, None) is True
