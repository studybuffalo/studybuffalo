"""Tests for the View module of the Substitutions app."""
# pylint: disable = too-many-lines
import importlib
import json
from unittest.mock import patch

import pytest

from django.test import Client, RequestFactory
from django.urls import reverse

from dictionary.models import Word, ExcludedWord
from hc_dpd.models import SubBrandPend
from substitutions import views, models
from substitutions.tests import utils

pytestmark = pytest.mark.django_db


# Function mocks to use during testing
def mock_dictionary_check(dictionary, value):
    """Mocks the dictionary_check function."""
    return f'TEST FUNCTION: dictionary = {dictionary}; value = {value}'


def mock_delete_entry(app_id, pend_id):
    """Mocks the delete_entry function."""
    return {'content': f'TEST FUNCTION: app_id = {app_id}; pend_id = {pend_id}'}


def mock_retrieve_pending_entries(app_id, last_id, request_num):
    """Mocks the retrieve_pending_entries function."""
    return {'content': f'TEST FUNCTION: app_id = {app_id}; last_id = {last_id}; request_num = {request_num}'}


def mock_retrieve_pending_entries_lookup_error(app_id, last_id, request_num):
    """Mocks the retrieve_pending_entries function to return lookup error."""
    raise LookupError(f'TEST FUNCTION: app_id = {app_id}; last_id = {last_id}; request_num = {request_num}')


def mock_add_new_substitutions(app_id, pend_id, orig, subs):
    """Mocks the add_new_substitutions function."""
    return {'content': f'TEST FUNCTION: app_id = {app_id}; pend_id = {pend_id}; orig = {orig}; subs = {subs}'}

# Patches to use during testing
patch_permission = patch(
    'django.contrib.auth.decorators.permission_required',
    lambda *args, **kwargs: lambda x: x
)

patch_delete_entry = patch('substitutions.views.delete_entry', mock_delete_entry)

patch_retrieve_pending_entries = patch('substitutions.views.retrieve_pending_entries', mock_retrieve_pending_entries)

patch_retrieve_pending_entries_lookup_error = patch(
    'substitutions.views.retrieve_pending_entries',
    mock_retrieve_pending_entries_lookup_error,
)

patch_add_new_substitutions = patch('substitutions.views.add_new_substitutions', mock_add_new_substitutions)


def test__binary_search__word_present__first():
    """Tests returns True when word present in search list at start."""
    search_list = ['bar', 'baz', 'foo']

    assert views.binary_search(search_list, 'bar') is True


def test__binary_search__word_present__middle():
    """Tests returns True when word present in search list in middle."""
    search_list = ['bar', 'baz', 'foo']

    assert views.binary_search(search_list, 'baz') is True


def test__binary_search__word_present__last():
    """Tests returns True when word present in search list at end."""
    search_list = ['bar', 'baz', 'foo']

    assert views.binary_search(search_list, 'foo') is True


def test__binary_search__word_present__not_present():
    """Tests returns None when word not present in search list."""
    search_list = ['bar', 'baz', 'foo']

    assert views.binary_search(search_list, 'apple') is None


def test__setup_dictionary(dictionary_word, dictionary_excluded_word):
    """Tests ouptut of the setup_dictiony function."""
    # Create additional word for testing
    Word.objects.create(
        dictionary_type=dictionary_word.dictionary_type,
        language=dictionary_word.language,
        dictionary_class=dictionary_word.dictionary_class,
        word='Test 2'
    )

    # Create additional excluded word for testing
    ExcludedWord.objects.create(
        dictionary_type=dictionary_excluded_word.dictionary_type,
        language=dictionary_excluded_word.language,
        dictionary_class=dictionary_excluded_word.dictionary_class,
        word='Excluded Test 2'
    )

    # Create duplicate excluding word to ensure this is removed
    ExcludedWord.objects.create(
        dictionary_type=dictionary_word.dictionary_type,
        language=dictionary_word.language,
        dictionary_class=dictionary_word.dictionary_class,
        word='Test 2'
    )

    # Get dictionary
    dictionary = views.setup_dictionary()

    # Confirm words are present in set
    assert isinstance(dictionary, list)
    assert len(dictionary) == 4
    assert 'Test 2' in dictionary
    assert 'Excluded Test 2' in dictionary


def test__dictionary_check__one_word__in_dictionary():
    """Tests handling for one word found in dictionary."""
    dictionary = ['bar', 'baz', 'foo']
    response = views.dictionary_check(dictionary, 'foo')

    assert response == 'foo'


def test__dictionary_check__two_words__in_dictionary():
    """Tests handling for two words found in dictionary."""
    dictionary = ['bar', 'baz', 'foo']
    response = views.dictionary_check(dictionary, 'foo bar')

    assert response == 'foo bar'


def test__dictionary_check__one_word__not_in_dictionary():
    """Tests handling for one word not found in dictionary."""
    dictionary = ['bar', 'baz', 'foo']
    response = views.dictionary_check(dictionary, 'apple')

    assert response == '<span class="missing">apple</span>'


def test__dictionary_check__one_word_of_two__not_in_dictionary():
    """Tests handling for one word of two not found in dictionary."""
    dictionary = ['bar', 'baz', 'foo']
    response = views.dictionary_check(dictionary, 'foo apple')

    assert response == 'foo <span class="missing">apple</span>'


def test__dictionary_check__two_words__not_in_dictionary():
    """Tests handling for two words not found in dictionary."""
    dictionary = ['bar', 'baz', 'foo']
    response = views.dictionary_check(dictionary, 'orange apple')

    assert response == '<span class="missing">orange</span> <span class="missing">apple</span>'


def test__dictionary_check__handles_apostrophe():
    """Tests handling for word with apostrophe."""
    dictionary = ['bar', 'baz', 'foo\'s']
    response = views.dictionary_check(dictionary, 'foo\'s')

    assert response == 'foo\'s'


def test__delete_entry__valid_deletion__output(hc_dpd_sub_brand_pend):
    """Tests delete_entry output for a successful deletion.

        Uses the HC DPD app SubBrand model for these tests.
    """
    pend_id =  hc_dpd_sub_brand_pend.pk

    # Create apps instance for testing
    apps = models.Apps.objects.create(
        app_name = 'hc_dpd',
        model_pending = 'SubBrandPend',
        model_sub = 'SubBrand',
    )

    response = views.delete_entry(apps.pk, pend_id)

    assert isinstance(response, dict)
    assert 'id' in response
    assert response['id'] == pend_id
    assert 'status_code' in response
    assert response['status_code'] == 204
    assert 'success' in response
    assert response['success'] is True
    assert 'message' in response
    assert response['message'] == f'Pending entry (id = {pend_id}) successfully deleted'


def test__delete_entry__valid_deletion__confirm_deletion(hc_dpd_sub_brand_pend):
    """Tests delete_entry for proper deletion.

        Uses the HC DPD app SubBrand model for these tests.
    """
    pend_id =  hc_dpd_sub_brand_pend.pk

    # Create apps instance for testing
    apps = models.Apps.objects.create(
        app_name = 'hc_dpd',
        model_pending = 'SubBrandPend',
        model_sub = 'SubBrand',
    )

    views.delete_entry(apps.pk, pend_id)

    # Confirm model instance no longer exists
    assert SubBrandPend.objects.filter(pk=pend_id).exists() is False


def test__delete_entry__handles_nonexistent_instance(hc_dpd_sub_brand_pend):
    """Tests delete_entry for handling nonexistent instance.

        Uses the HC DPD app SubBrand model for these tests.
    """
    pend_id =  hc_dpd_sub_brand_pend.pk

    # Delete pending entry
    hc_dpd_sub_brand_pend.delete()

    # Create apps instance for testing
    apps = models.Apps.objects.create(
        app_name = 'hc_dpd',
        model_pending = 'SubBrandPend',
        model_sub = 'SubBrand',
    )

    response = views.delete_entry(apps.pk, pend_id)

    assert isinstance(response, dict)
    assert 'id' in response
    assert response['id'] == pend_id
    assert 'status_code' in response
    assert response['status_code'] == 400
    assert 'success' in response
    assert response['success'] is False
    assert 'errors' in response
    assert response['errors'] == ['Unable to delete pending entry: SubBrandPend matching query does not exist.']


def test__delete_entry__handles_nonexistent_model():
    """Tests delete_entry for handling nonexistent model.

        Uses the HC DPD app SubBrand model for these tests.
    """
    # Create apps instance for testing
    apps = models.Apps.objects.create(
        app_name = 'Fake',
        model_pending = 'FakeModelPend',
        model_sub = 'FakeModel',
    )

    response = views.delete_entry(apps.pk, 1)

    assert isinstance(response, dict)
    assert 'id' in response
    assert response['id'] == 1
    assert 'status_code' in response
    assert response['status_code'] == 400
    assert 'success' in response
    assert response['success'] is False
    assert 'errors' in response
    assert response['errors'] == ['Unable to locate model: FakeModelPend']


def test__retrieve_pending_entries__output(hc_dpd_sub_brand_pend):
    """Tests retrieve_pending_entries output format.

        Uses the HC DPD app SubBrand model for these tests.
    """
    pend_id = hc_dpd_sub_brand_pend.pk

    # Create apps instance for testing
    apps = models.Apps.objects.create(
        app_name = 'hc_dpd',
        model_pending = 'SubBrandPend',
        model_sub = 'SubBrand',
    )
    models.ModelFields.objects.create(
        app=apps,
        field_name='original',
        field_type='o',
        dictionary_check=False,
        google_check=False,
    )
    models.ModelFields.objects.create(
        app=apps,
        field_name='substitution',
        field_type='s',
        dictionary_check=False,
        google_check=False,
    )
    response = views.retrieve_pending_entries(apps.pk, pend_id - 1, 10)

    assert isinstance(response, dict)
    assert 'content' in response
    assert isinstance(response['content'], list)
    assert isinstance(response['status_code'], int)
    assert response['status_code'] == 200

    assert 'id' in response['content'][0]
    assert isinstance(response['content'][0]['id'], int)
    assert response['content'][0]['id'] == pend_id
    assert 'orig' in response['content'][0]
    assert isinstance(response['content'][0]['orig'], list)
    assert 'subs' in response['content'][0]
    assert isinstance(response['content'][0]['subs'], list)

    assert 'field_name' in response['content'][0]['orig'][0]
    assert isinstance(response['content'][0]['orig'][0]['field_name'], str)
    assert response['content'][0]['orig'][0]['field_name'] == 'original'
    assert 'google' in response['content'][0]['orig'][0]
    assert isinstance(response['content'][0]['orig'][0]['google'], bool)
    assert response['content'][0]['orig'][0]['google'] is False
    assert 'value' in response['content'][0]['orig'][0]
    assert isinstance(response['content'][0]['orig'][0]['value'], str)
    assert response['content'][0]['orig'][0]['value'] == 'Original Brand 1 Pending'

    assert 'field_name' in response['content'][0]['subs'][0]
    assert isinstance(response['content'][0]['subs'][0]['field_name'], str)
    assert response['content'][0]['subs'][0]['field_name'] == 'substitution'
    assert 'google' in response['content'][0]['subs'][0]
    assert isinstance(response['content'][0]['subs'][0]['google'], bool)
    assert response['content'][0]['subs'][0]['google'] is False
    assert 'value' in response['content'][0]['subs'][0]
    assert isinstance(response['content'][0]['subs'][0]['value'], str)
    assert response['content'][0]['subs'][0]['value'] == 'Sub Brand 1 Pending'


@patch('substitutions.views.dictionary_check', mock_dictionary_check)
def test__retrieve_pending_entries__dictionary_check_runs(hc_dpd_sub_brand_pend):
    """Tests retrieve_pending_entries calls dictionary_check.

        Uses the HC DPD app SubBrand model for these tests.
    """
    pend_id = hc_dpd_sub_brand_pend.pk

    # Create apps instance for testing
    apps = models.Apps.objects.create(
        app_name = 'hc_dpd',
        model_pending = 'SubBrandPend',
        model_sub = 'SubBrand',
    )
    models.ModelFields.objects.create(
        app=apps,
        field_name='original',
        field_type='o',
        dictionary_check=True,
        google_check=False,
    )
    models.ModelFields.objects.create(
        app=apps,
        field_name='substitution',
        field_type='s',
        dictionary_check=True,
        google_check=False,
    )
    response = views.retrieve_pending_entries(apps.pk, pend_id - 1, 10)

    assert 'TEST FUNCTION' in response['content'][0]['orig'][0]['value']
    assert 'TEST FUNCTION' in response['content'][0]['subs'][0]['value']


def test__add_new_substitutions__valid_addition(hc_dpd_sub_brand_pend):
    """Tests add_new_substitutions output for a successful addition.

        Uses the HC DPD app SubBrand model for these tests.
    """
    pend_id =  hc_dpd_sub_brand_pend.pk

    # Create apps instance for testing
    apps = models.Apps.objects.create(
        app_name = 'hc_dpd',
        model_pending = 'SubBrandPend',
        model_sub = 'SubBrand',
    )

    # Data for substitution
    orig = json.dumps([{
        'field_name': 'original',
        'field_value': 'New original'
    }])
    subs = json.dumps([{
        'field_name': 'substitution',
        'field_value': 'New sub'
    }])

    response = views.add_new_substitutions(apps.pk, pend_id, orig, subs)

    assert isinstance(response, dict)
    assert 'id' in response
    assert response['id'] == pend_id
    assert 'success' in response
    assert response['success'] is True
    assert 'message' in response
    assert response['message'] == 'New substitution added (Health Canada Drug Product Database)'


def test__add_new_substitutions__invalid_orig_data(hc_dpd_sub_brand_pend):
    """Tests add_new_substitutions for handling invalid orig data.

        Uses the HC DPD app SubBrand model for these tests.
    """
    pend_id =  hc_dpd_sub_brand_pend.pk

    # Create apps instance for testing
    apps = models.Apps.objects.create(
        app_name = 'hc_dpd',
        model_pending = 'SubBrandPend',
        model_sub = 'SubBrand',
    )

    # Data for substitution
    orig = json.dumps([{
        'field_name': 'ERROR',
        'field_value': 'New original'
    }])
    subs = json.dumps([{
        'field_name': 'substitution',
        'field_value': 'New sub'
    }])

    response = views.add_new_substitutions(apps.pk, pend_id, orig, subs)

    assert isinstance(response, dict)
    assert 'id' in response
    assert response['id'] == pend_id
    assert 'success' in response
    assert response['success'] is False
    assert 'message' in response
    assert response['message'] == 'Unable to save new substitution: No original field name ERROR'


def test__add_new_substitutions__invalid_sub_data(hc_dpd_sub_brand_pend):
    """Tests add_new_substitutions for handling invalid sub data.

        Uses the HC DPD app SubBrand model for these tests.
    """
    pend_id =  hc_dpd_sub_brand_pend.pk

    # Create apps instance for testing
    apps = models.Apps.objects.create(
        app_name = 'hc_dpd',
        model_pending = 'SubBrandPend',
        model_sub = 'SubBrand',
    )

    # Data for substitution
    orig = json.dumps([{
        'field_name': 'original',
        'field_value': 'New original'
    }])
    subs = json.dumps([{
        'field_name': 'ERROR',
        'field_value': 'New sub'
    }])

    response = views.add_new_substitutions(apps.pk, pend_id, orig, subs)

    assert isinstance(response, dict)
    assert 'id' in response
    assert response['id'] == pend_id
    assert 'success' in response
    assert response['success'] is False
    assert 'message' in response
    assert response['message'] == 'Unable to save new substitution: No substitution field name ERROR'


def test__add_new_substitutions__invalid_model(hc_dpd_sub_brand_pend):
    """Tests add_new_substitutions for handling invalid model data.

        Uses the HC DPD app SubBrand model for these tests.
    """
    pend_id =  hc_dpd_sub_brand_pend.pk

    # Create apps instance for testing
    apps = models.Apps.objects.create(
        app_name = 'hc_dpd',
        model_pending = 'SubBrandPend',
        model_sub = 'ERROR',
    )

    # Data for substitution
    orig = json.dumps([{
        'field_name': 'original',
        'field_value': 'New original'
    }])
    subs = json.dumps([{
        'field_name': 'substitution',
        'field_value': 'New sub'
    }])

    response = views.add_new_substitutions(apps.pk, pend_id, orig, subs)

    assert isinstance(response, dict)
    assert 'id' in response
    assert response['id'] == pend_id
    assert 'success' in response
    assert response['success'] is False
    assert 'message' in response
    assert response['message'] == 'Unable to locate model: hc_dpd.ERROR'


def test__delete_pend__204_response():
    """Confirms add new word view returns 204 response."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_delete_entry.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'app_id': 1, 'pend_id': 2}
    response = views.delete_pend(request)

    # Confirm status code
    assert response.status_code == 204

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'content' in content
    assert 'TEST FUNCTION' in content['content']

    # Stop permission patch
    patch_permission.stop()
    patch_delete_entry.stop()
    importlib.reload(views)


def test__delete_pend__400_response__missing_app_id():
    """Confirms 400 response when no app_id."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_delete_entry.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'pend_id': 2}
    response = views.delete_pend(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'id' in content
    assert content['id'] is None
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 400
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Request missing arguments: app_id']

    # Stop permission patch
    patch_permission.stop()
    patch_delete_entry.stop()
    importlib.reload(views)


def test__delete_pend__400_response__missing_pend_id():
    """Confirms 400 response when no pend_id."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_delete_entry.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'app_id': 1}
    response = views.delete_pend(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'id' in content
    assert content['id'] is None
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 400
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Request missing arguments: pend_id']

    # Stop permission patch
    patch_permission.stop()
    patch_delete_entry.stop()
    importlib.reload(views)


def test__delete_pend__400_response__missing_all_data():
    """Confirms 400 response when no POST data."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_delete_entry.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {}
    response = views.delete_pend(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'id' in content
    assert content['id'] is None
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 400
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Request missing arguments: app_id, pend_id']

    # Stop permission patch
    patch_permission.stop()
    patch_delete_entry.stop()
    importlib.reload(views)


def test__delete_pend__405_response():
    """Confirms 405 response when incorrect request method."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_delete_entry.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'GET'
    response = views.delete_pend(request)

    # Confirm status code
    assert response.status_code == 405

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'id' in content
    assert content['id'] is None
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 405
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Only "POST" method is allowed.']

    # Stop permission patch
    patch_permission.stop()
    patch_delete_entry.stop()
    importlib.reload(views)


def test__retrieve_entries__200_response():
    """Confirms retrieve entries view returns 200 response."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_retrieve_pending_entries.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'app_id': 1, 'last_id': 2, 'request_num': 3}
    response = views.retrieve_entries(request)

    # Confirm status code
    assert response.status_code == 200

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'content' in content
    assert 'TEST FUNCTION' in content['content']

    # Stop permission patch
    patch_permission.stop()
    patch_retrieve_pending_entries.stop()
    importlib.reload(views)


def test__retrieve_entrires__handles_nonexistent_model():
    """Tests retrieve_entries for handling nonexistent model.

        Uses the HC DPD app SubBrand model for these tests.
    """
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_retrieve_pending_entries_lookup_error.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'app_id': 1, 'last_id': 2, 'request_num': 3}
    response = views.retrieve_entries(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 400
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Unable to locate model for app_id = 1']

    # Stop permission patch
    patch_permission.stop()
    patch_retrieve_pending_entries_lookup_error.stop()
    importlib.reload(views)


def test__retrieve_entries__400_response__missing_app_id():
    """Confirms 400 response when no app_id."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_retrieve_pending_entries.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'last_id': 2, 'request_num': 3}
    response = views.retrieve_entries(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 400
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Request missing arguments: app_id']

    # Stop permission patch
    patch_permission.stop()
    patch_retrieve_pending_entries.stop()
    importlib.reload(views)


def test__retrieve_entries__400_response__missing_last_id():
    """Confirms 400 response when no last_id."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_retrieve_pending_entries.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'app_id': 1, 'request_num': 3}
    response = views.retrieve_entries(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 400
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Request missing arguments: last_id']

    # Stop permission patch
    patch_permission.stop()
    patch_retrieve_pending_entries.stop()
    importlib.reload(views)


def test__retrieve_entries__400_response__missing_request_num():
    """Confirms 400 response when no request_num."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_retrieve_pending_entries.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'app_id': 1, 'last_id': 2}
    response = views.retrieve_entries(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 400
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Request missing arguments: request_num']

    # Stop permission patch
    patch_permission.stop()
    patch_retrieve_pending_entries.stop()
    importlib.reload(views)


def test__retrieve_entries__400_response__missing_all_data():
    """Confirms 400 response when no POST data."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_retrieve_pending_entries.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {}
    response = views.retrieve_entries(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 400
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Request missing arguments: app_id, last_id, request_num']

    # Stop permission patch
    patch_permission.stop()
    patch_retrieve_pending_entries.stop()
    importlib.reload(views)


def test__retrieve_entries__405_response():
    """Confirms 405 response from retrieve entries with incorrect method."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_retrieve_pending_entries.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'GET'
    response = views.retrieve_entries(request)

    # Confirm status code
    assert response.status_code == 405

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 405
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Only "POST" method is allowed.']

    # Stop permission patch
    patch_permission.stop()
    patch_retrieve_pending_entries.stop()
    importlib.reload(views)


def test__verify__201_response():
    """Confirms verify view returns 201 response."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_add_new_substitutions.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'app_id': 1, 'pend_id': 2, 'orig': 3, 'subs': 4}
    response = views.verify(request)

    # Confirm status code
    assert response.status_code == 201

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'content' in content
    assert 'TEST FUNCTION' in content['content']

    # Stop permission patch
    patch_permission.stop()
    patch_add_new_substitutions.stop()
    importlib.reload(views)


def test__verify__400_response__missing_app_id():
    """Confirms verify view returns 400 response with missing app_id."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_add_new_substitutions.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'pend_id': 2, 'orig': 3, 'subs': 4}
    response = views.verify(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 400
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Request missing arguments: app_id']

    # Stop permission patch
    patch_permission.stop()
    patch_add_new_substitutions.stop()
    importlib.reload(views)


def test__verify__400_response__missing_pend_id():
    """Confirms verify view returns 400 response with missing pend_id."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_add_new_substitutions.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'app_id': 1, 'orig': 3, 'subs': 4}
    response = views.verify(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 400
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Request missing arguments: pend_id']

    # Stop permission patch
    patch_permission.stop()
    patch_add_new_substitutions.stop()
    importlib.reload(views)



def test__verify__400_response__missing_orig():
    """Confirms verify view returns 400 response with missing orig."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_add_new_substitutions.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'app_id': 1, 'pend_id': 2, 'subs': 4}
    response = views.verify(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 400
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Request missing arguments: orig']

    # Stop permission patch
    patch_permission.stop()
    patch_add_new_substitutions.stop()
    importlib.reload(views)



def test__verify__400_response__missing_subs():
    """Confirms verify view returns 400 response with missing subs."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_add_new_substitutions.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'app_id': 1, 'pend_id': 2, 'orig': 3}
    response = views.verify(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 400
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Request missing arguments: subs']


    # Stop permission patch
    patch_permission.stop()
    patch_add_new_substitutions.stop()
    importlib.reload(views)


def test__verify__400_response__missing_all_data():
    """Confirms verify view returns 400 response with missing POST data."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_add_new_substitutions.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {}
    response = views.verify(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 400
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Request missing arguments: app_id, pend_id, orig, subs']

    # Stop permission patch
    patch_permission.stop()
    patch_add_new_substitutions.stop()
    importlib.reload(views)


def test__verify__405_response():
    """Confirms 405 response from verify view with incorrect method."""
    # Start required patches
    patch_permission.start()
    importlib.reload(views)
    patch_add_new_substitutions.start()

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'GET'
    response = views.verify(request)

    # Confirm status code
    assert response.status_code == 405

    # Confirm content is attached to response
    content = json.loads(response.content)
    assert 'success' in content
    assert content['success'] is False
    assert 'status_code' in content
    assert isinstance(content['status_code'], int)
    assert content['status_code'] == 405
    assert 'errors' in content
    assert isinstance(content['errors'], list)
    assert content['errors'] == ['Only "POST" method is allowed.']

    # Stop permission patch
    patch_permission.stop()
    patch_add_new_substitutions.stop()
    importlib.reload(views)


def test__review__200_response(user):
    """Confirms review view returns 200 response."""
    # Create apps instance for testing
    apps = models.Apps.objects.create(
        app_name = 'hc_dpd',
        model_pending = 'SubBrandPend',
        model_sub = 'SubBrand',
    )

    # Add user permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Get response
    response = client.get(reverse('sub_review', kwargs={'app_id': apps.pk}))

    # Confirm status code
    assert response.status_code == 200


def test__review__context(user):
    """Confirms review view returns expected context details.

        Need to load permissions properly here to get full response
        context.
    """
    # Create apps instance for testing
    apps = models.Apps.objects.create(
        app_name = 'hc_dpd',
        model_pending = 'SubBrandPend',
        model_sub = 'SubBrand',
    )

    # Add user permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Get response
    response = client.get(reverse('sub_review', kwargs={'app_id': apps.pk}))

    # Test for context key
    assert 'app_data' in response.context

    # Confirm proper data
    assert response.context['app_data'] == {
        'id': apps.pk,
        'app_name': apps.app_name,
        'pending': apps.model_pending,
        'sub': apps.model_sub,
    }


def test__review__template(user):
    """Confirms review view returns expected template."""
    # Create apps instance for testing
    apps = models.Apps.objects.create(
        app_name = 'hc_dpd',
        model_pending = 'SubBrandPend',
        model_sub = 'SubBrand',
    )

    # Add user permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Get response
    response = client.get(reverse('sub_review', kwargs={'app_id': apps.pk}))

    # Test for template
    assert 'substitutions/review.html' in [t.name for t in response.templates]


def test__dashboard__200_response(user, substitutions_apps):  # pylint: disable=unused-argument
    """Confirms dashboard view returns 200 response."""
    # Add user permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Get response
    response = client.get(reverse('sub_dashboard'))

    # Confirm status code
    assert response.status_code == 200


def test__dashboard__context(user):
    """Confirms dashboard view returns expected context details.

        Need to load permissions properly here to get full response
        context.
    """
    # Create apps instance for testing
    apps = models.Apps.objects.create(
        app_name = 'hc_dpd',
        model_pending = 'SubBrandPend',
        model_sub = 'SubBrand',
    )

    # Add user permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Get response
    response = client.get(reverse('sub_dashboard'))

    # Test for context key
    assert 'sub_data' in response.context

    # Confirm proper data
    assert response.context['sub_data'] == {
        'hc_dpd': {
            'app_name': 'Health Canada Drug Product Database',
            'data': [{
                'count': 0,
                'id': apps.id,
                'pending': 'Substitution - Brand Name (Pending)',
                'sub': 'SubBrand',
            }],
        }
    }


def test__dashboard__template(user, substitutions_apps):  # pylint: disable=unused-argument
    """Confirms dashboard view returns expected template."""
    # Create apps instance for testing
    models.Apps.objects.create(
        app_name = 'hc_dpd',
        model_pending = 'SubBrandPend',
        model_sub = 'SubBrand',
    )

    # Add user permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Get response
    response = client.get(reverse('sub_dashboard'))

    # Test for template
    assert 'substitutions/dashboard.html' in [t.name for t in response.templates]
