"""Tests for the Model module of the Substitutions app."""
from unittest.mock import patch

import pytest

from django.test import Client
from django.urls import reverse

from substitutions.tests import utils

pytestmark = pytest.mark.django_db


def mock_delete_entry(app_id, pend_id):
    """Mocking delete_entry to allow unit-testing."""
    return {
        'id': pend_id,
        'status_code': 204,
        'success': True,
        'message': f'App ID = {app_id}; Pend ID = {pend_id}'
    }


def mock_retrieve_pending_entries(app_id, last_id, request_num):
    """Mocking retrieve_pending_entries to allow unit-testing."""
    return {
        'status_code': 200,
        'content': [{
            'app_id': app_id,
            'last_id': last_id,
            'request_num': request_num,
        }]
    }


def mock_add_new_substitutions(app_id, pend_id, orig, subs):
    """Mocking add_new_substitutions to allow unit-testing."""
    return {
        'id': pend_id,
        'success': True,
        'status_code': 200,
        'messsage': f'app_id = {app_id}; pend_id = {pend_id}; orig = {orig}; subs={subs}'
    }


@patch('substitutions.views.delete_entry', mock_delete_entry)
def test__delete_entry__exists_at_desired_url(user):
    """Tests delete entry page exists at desired URL."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request
    post_data = {'app_id': 1, 'pend_id': 1}
    response = client.post(
        '/tools/substitutions/review/delete-entry/',
        post_data
    )

    assert response.status_code == 204


@patch('substitutions.views.delete_entry', mock_delete_entry)
def test__delete_entry__url_name(user):
    """Tests delete entry page URL name."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request
    post_data = {'app_id': 1, 'pend_id': 1}
    response = client.post(reverse('sub_delete_entry'), post_data)

    assert response.status_code == 204


@patch('substitutions.views.delete_entry', mock_delete_entry)
def test__delete_entry__302_on_user_without_permissions(user):
    """Tests delete entry page returns 302 for user without permission."""
    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request
    post_data = {'app_id': 1, 'pend_id': 1}
    response = client.post(reverse('sub_delete_entry'), post_data)

    assert response.status_code == 302


@patch('substitutions.views.delete_entry', mock_delete_entry)
def test__delete_entry__302_on_anonymous_user():
    """Tests delete entry page returns 302 for anonymous user."""
    # Create client
    client = Client()

    # Test POST request
    post_data = {'app_id': 1, 'pend_id': 1}
    response = client.post(reverse('sub_delete_entry'), post_data)

    assert response.status_code == 302


@patch('substitutions.views.retrieve_pending_entries', mock_retrieve_pending_entries)
def test__retrieve_entry__exists_at_desired_url(user):
    """Tests retrieve entry page exists at desired URL."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request
    post_data = {'app_id': 1, 'last_id': 1, 'request_num': 1}
    response = client.post(
        '/tools/substitutions/review/retrieve-entries/',
        post_data
    )

    assert response.status_code == 200


@patch('substitutions.views.retrieve_pending_entries', mock_retrieve_pending_entries)
def test__retrieve_entry__url_name(user):
    """Tests retrieve entry page URL name."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request
    post_data = {'app_id': 1, 'last_id': 1, 'request_num': 1}
    response = client.post(reverse('sub_retrieve_entry'), post_data)

    assert response.status_code == 200


@patch('substitutions.views.retrieve_pending_entries', mock_retrieve_pending_entries)
def test__retrieve_entry__302_on_user_without_permissions(user):
    """Tests retrieve entry page returns 302 for user without permission."""
    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request
    post_data = {'app_id': 1, 'last_id': 1, 'request_num': 1}
    response = client.post(reverse('sub_retrieve_entry'), post_data)

    assert response.status_code == 302


@patch('substitutions.views.retrieve_pending_entries', mock_retrieve_pending_entries)
def test__retrieve_entry__302_on_anonymous_user():
    """Tests retrieve entry page returns 302 for anonymous user."""
    # Create client
    client = Client()

    # Test POST request
    post_data = {'app_id': 1, 'last_id': 1, 'request_num': 1}
    response = client.post(reverse('sub_retrieve_entry'), post_data)

    assert response.status_code == 302


@patch('substitutions.views.add_new_substitutions', mock_add_new_substitutions)
def test__verify_entry__exists_at_desired_url(user, substitutions_apps):
    """Tests verify entry page exists at desired URL."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request
    post_data = {
        'app_id': substitutions_apps.pk,
        'pend_id': 1,
        'orig': {'orig': 'test'},
        'subs': {'subs': 'test'},
    }
    response = client.post(
        '/tools/substitutions/review/verify-entry/',
        post_data,
    )

    assert response.status_code == 201


@patch('substitutions.views.add_new_substitutions', mock_add_new_substitutions)
def test__verify_entry__url_name(user, substitutions_apps):
    """Tests verify entry page URL name."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request

    # Test POST request
    post_data = {
        'app_id': substitutions_apps.pk,
        'pend_id': 1,
        'orig': {'orig': 'test'},
        'subs': {'subs': 'test'},
    }
    response = client.post(reverse('sub_verify_entry'), post_data)

    assert response.status_code == 201


@patch('substitutions.views.add_new_substitutions', mock_add_new_substitutions)
def test__verify_entry__302_on_user_without_permissions(user, substitutions_apps):
    """Tests that add new entries page returns 302 for user without permission."""
    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request
    post_data = {
        'app_id': substitutions_apps.pk,
        'pend_id': 1,
        'orig': {'orig': 'test'},
        'subs': {'subs': 'test'},
    }
    response = client.post(reverse('sub_verify_entry'), post_data)

    assert response.status_code == 302


@patch('substitutions.views.add_new_substitutions', mock_add_new_substitutions)
def test__verify_entry__302_on_anonymous_user(substitutions_apps):
    """Tests that add new entries page returns 302 for anonymous user."""
    # Create client
    client = Client()

    # Test POST request
    post_data = {
        'app_id': substitutions_apps.pk,
        'pend_id': 1,
        'orig': {'orig': 'test'},
        'subs': {'subs': 'test'},
    }
    response = client.post(reverse('sub_verify_entry'), post_data)

    assert response.status_code == 302


def test__review__exists_at_desired_url(user, substitutions_apps):
    """Tests review page exists at desired URL."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test GET request
    response = client.get(f'/tools/substitutions/review/{substitutions_apps.pk}/')

    assert response.status_code == 200


def test__review__url_name(user, substitutions_apps):
    """Tests review page URL name works."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test GET request
    response = client.get(reverse(
        'sub_review',
        kwargs={'app_id': substitutions_apps.pk}
    ))

    assert response.status_code == 200


def test__review__302_on_user_without_permissions(user, substitutions_apps):
    """Tests review page returns 302 for user without permission."""
    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test GET request
    response = client.get(reverse(
        'sub_review',
        kwargs={'app_id': substitutions_apps.pk}
    ))

    assert response.status_code == 302


def test__review__302_on_anonymous_user(substitutions_apps):
    """Tests that review entries page returns 302 for anonymous user."""
    # Create client
    client = Client()

    # Test GET request
    response = client.get(reverse(
        'sub_review',
        kwargs={'app_id': substitutions_apps.pk}
    ))

    assert response.status_code == 302


def test__dashboard__exists_at_desired_url(user):
    """Tests that dashboard page exists at desired URL."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test GET request
    response = client.get('/tools/substitutions/')

    assert response.status_code == 200


def test__dashboard__url_name(user):
    """Tests that dashboard page URL name works."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test GET request
    response = client.get(reverse('sub_dashboard'))

    assert response.status_code == 200
