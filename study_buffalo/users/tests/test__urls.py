"""Tests for the User URLs."""
import pytest

from django.urls import reverse, resolve


pytestmark = pytest.mark.django_db

def test__user_list__reverse():
    """Tests the users:list revers URL."""
    assert reverse('users:list') == '/users/'

def test__user_list__resolve():
    """Tests that /users/ resolves to users:list."""
    assert resolve('/users/').view_name == 'users:list'

def test__user_redirect__reverse():
    """Tests that users:redirect reverses to /users/~redirect/."""
    assert reverse('users:redirect') == '/users/~redirect/'

def test__user_redirect_resolve():
    """Tests that /users/~redirect/ resolves to users:redirect."""
    assert resolve('/users/~redirect/').view_name == 'users:redirect'

def test__user_detail__reverse(user):
    """Tests that users:detail reverses to /users/<username>/."""
    assert reverse('users:detail', kwargs={'username': user.username}) == f'/users/{user.username}/'

def test__user_detail__resolve(user):
    """Tests that /users/<username>/ resolves to users:detail."""
    assert resolve(f'/users/{user.username}/').view_name == 'users:detail'

def test__user_update__reverse():
    """Tests that users:update reverses to /users/~update/."""
    assert reverse('users:update') == '/users/~update/'

def test__user_update__resolve():
    """Tests thtat /users/~update/ resolves to users:update."""
    assert resolve('/users/~update/').view_name == 'users:update'
