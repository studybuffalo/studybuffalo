"""Tests for the URLs module of the Dictionary app."""
import pytest

from django.test import Client
from django.urls import reverse

from dictionary.tests import utils

pytestmark = pytest.mark.django_db


def test__review__exists_at_desired_url(user):
    """Tests that dictionary review page exists at desired URL."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test GET request
    response = client.get('/tools/dictionary/review/')

    assert response.status_code == 200


def test__review__url_name(user):
    """Tests that dictionary review page URL name works."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test GET request
    response = client.get(reverse('dictionary_review'))

    assert response.status_code == 200


def test__review__302_on_user_without_permissions(user):
    """Tests that review entries page returns 302 for user without permission."""
    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test GET request
    response = client.get(reverse('dictionary_review'))

    assert response.status_code == 302


def test__review__302_on_anonymous_user():
    """Tests that review entries page returns 302 for anonymous user."""
    # Create client
    client = Client()

    # Test GET request
    response = client.get(reverse('dictionary_review'))

    assert response.status_code == 302


def test__retrieve_entries__exists_at_desired_url(user):
    """Tests that retrieve entries page exists at desired URL."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request
    response = client.post(
        '/tools/dictionary/review/retrieve-entries/',
        {'last_id': 1, 'request_num': 1},
    )

    assert response.status_code == 200


def test__retrieve_entries__url_name(user):
    """Tests that retrieve entries page URL name works."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request
    response = client.post(
        reverse('dictionary_retrieve_entry'),
        {'last_id': 1, 'request_num': 1},
    )

    assert response.status_code == 200


def test__retrieve_entries__302_on_user_without_permissions(user):
    """Tests that retrieve entries page returns 302 for user without permission."""
    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request
    response = client.post(
        reverse('dictionary_retrieve_entry'),
        {'last_id': 1, 'request_num': 1},
    )

    assert response.status_code == 302


def test__retrieve_entries__302_on_anonymous_user():
    """Tests that retrieve entries page returns 302 for anonymous user."""
    # Create client
    client = Client()

    # Test POST request
    response = client.post(
        reverse('dictionary_retrieve_entry'),
        {'last_id': 1, 'request_num': 1},
    )

    assert response.status_code == 302


def test__add_new_word__exists_at_desired_url(user, dictionary_word_pending):
    """Tests that add new word page exists at desired URL."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request
    post_data = {
        'pending_id': dictionary_word_pending.pk,
        'model_name': 'word',
        'word': 'abc',
        'language': dictionary_word_pending.language.pk,
        'dictionary_type': dictionary_word_pending.dictionary_type.pk,
        'dictionary_class': dictionary_word_pending.dictionary_class.pk,
    }
    response = client.post(
        '/tools/dictionary/review/add-new-word/',
        post_data,
    )

    assert response.status_code == 201


def test__add_new_word__302_on_user_without_permissions(user, dictionary_word_pending):
    """Tests that add new entries page returns 302 for user without permission."""
    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request
    post_data = {
        'pending_id': dictionary_word_pending.pk,
        'model_name': 'word',
        'word': 'abc',
        'language': dictionary_word_pending.language.pk,
        'dictionary_type': dictionary_word_pending.dictionary_type.pk,
        'dictionary_class': dictionary_word_pending.dictionary_class.pk,
    }
    response = client.post(
        '/tools/dictionary/review/add-new-word/',
        post_data,
    )

    assert response.status_code == 302


def test__add_new_word__302_on_anonymous_user(dictionary_word_pending):
    """Tests that add new entries page returns 302 for anonymous user."""
    # Create client
    client = Client()

    # Test POST request
    post_data = {
        'pending_id': dictionary_word_pending.pk,
        'model_name': 'word',
        'word': 'abc',
        'language': dictionary_word_pending.language.pk,
        'dictionary_type': dictionary_word_pending.dictionary_type.pk,
        'dictionary_class': dictionary_word_pending.dictionary_class.pk,
    }
    response = client.post(
        '/tools/dictionary/review/add-new-word/',
        post_data,
    )

    assert response.status_code == 302


def test__delete_pending_word__exists_at_desired_url(user, dictionary_word_pending):
    """Tests that delete pending word page exists at desired URL."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request
    post_data = {'pending_id': dictionary_word_pending.pk}
    response = client.post(
        '/tools/dictionary/review/delete-pending-word/',
        post_data,
    )

    assert response.status_code == 204


def test__delete_pending_word__302_on_user_without_permissions(user, dictionary_word_pending):
    """Tests that delete pending word page returns 302 for user without permission."""
    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test POST request
    post_data = {'pending_id': dictionary_word_pending.pk}
    response = client.post(
        '/tools/dictionary/review/delete-pending-word/',
        post_data,
    )

    assert response.status_code == 302


def test__delete_pending_word__302_on_anonymous_user(dictionary_word_pending):
    """Tests that delete pending page returns 302 for anonymous user."""
    # Create client
    client = Client()

    # Test POST request
    post_data = {'pending_id': dictionary_word_pending.pk}
    response = client.post(
        '/tools/dictionary/review/delete-pending-word/',
        post_data,
    )

    assert response.status_code == 302


def test__retrieve_select_data__exists_at_desired_url(user):
    """Tests that retrieve select data page exists at desired URL."""
    # Give user required permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test GET request
    response = client.get('/tools/dictionary/review/retrieve-select-data/')

    assert response.status_code == 200


def test__retrieve_select_data__302_on_user_without_permissions(user):
    """Tests that retrieve select data page returns 302 for user without permission."""
    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Test GET request
    response = client.get('/tools/dictionary/review/retrieve-select-data/')

    assert response.status_code == 302


def test__retrieve_select_data__302_on_anonymous_user():
    """Tests that retrieve select data page returns 302 for anonymous user."""
    # Create client
    client = Client()

    # Test GET request
    response = client.get('/tools/dictionary/review/retrieve-select-data/')

    assert response.status_code == 302



def test__index__exists_at_desired_url():
    """Tests that dictionary index page exists at desired URL."""
    client = Client()
    response = client.get('/tools/dictionary/')

    assert response.status_code == 200


def test__index__url_name():
    """Tests that dictionary index page URL name works."""
    client = Client()
    response = client.get(reverse('dictionary_index'))

    assert response.status_code == 200
