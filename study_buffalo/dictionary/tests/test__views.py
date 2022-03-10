"""Tests for the Views module of the Dictionary app."""
import importlib
import json
import re
from unittest.mock import patch

import pytest

from django.test import Client, RequestFactory
from django.urls import reverse

from dictionary import views, models
from dictionary.tests import utils


pytestmark = pytest.mark.django_db


# Patch to allow overriding permission decorator
permission_patch = patch(
    'django.contrib.auth.decorators.permission_required',
    lambda *args, **kwargs: lambda x: x
)


def test__index__200_resonse():
    """Confirms index view returns 200 response."""
    # Create request, view, and response
    request = RequestFactory()
    response = views.index(request)

    # Confirm status code
    assert response.status_code == 200


def test__index__template():
    """Confirms index view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('dictionary_index'))

    # Test for template
    assert (
        'dictionary/index.html' in [t.name for t in response.templates]
    )


def test__retrieve_select_data__200_response():
    """Confirms retrieve select data view returns 200 response."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    response = views.retrieve_select_data(request)

    # Confirm status code
    assert response.status_code == 200

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__retrieve_select_data__json_response():
    """Confirms retrieve select data view returns JSON response."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    response = views.retrieve_select_data(request)

    # Confirm content type
    assert response.headers['Content-Type'] == 'application/json'

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__generate_select_data__confirm_dictionary():
    """Confirms response returns expected dictionary."""
    selects = views.generate_select_data()

    # Confirm dictionary type returned
    assert isinstance(selects, dict)

    # Confirm expected keys present
    assert 'language' in selects
    assert 'dict_type' in selects
    assert 'dict_class' in selects

    # Confirm key values are strings
    assert isinstance(selects['language'], str)
    assert isinstance(selects['dict_type'], str)
    assert isinstance(selects['dict_class'], str)


def test__generate_select_data__language_details():
    """Confirms response returns expected language details."""
    # Create test languages
    language_1 = models.Language.objects.create(language='1')
    language_2 = models.Language.objects.create(language='2')

    selects = views.generate_select_data()
    language_select = selects['language']

    # Confirm options are present as expected
    option_1 = f'<option value="{language_1.id}">{language_1.language}</option>'
    option_2 = f'<option value="{language_2.id}">{language_2.language}</option>'

    assert option_1 in language_select
    assert option_2 in language_select

    # Confirm proper select tags are present
    select_regex = re.compile(r'^<select class=\"language\">.*<\/select>$')
    assert select_regex.match(language_select)


def test__generate_select_data__dictionary_type_details():
    """Confirms response returns expected dictionary type details."""
    # Create test languages
    type_1 = models.DictionaryType.objects.create(
        dictionary_name='1',
        dictionary_verbose_name='One',
    )
    type_2 = models.DictionaryType.objects.create(
        dictionary_name='2',
        dictionary_verbose_name='Two',
    )

    selects = views.generate_select_data()
    type_select = selects['dict_type']

    # Confirm options are present as expected
    option_1 = f'<option value="{type_1.id}">{type_1.dictionary_name}</option>'
    option_2 = f'<option value="{type_2.id}">{type_2.dictionary_name}</option>'

    assert option_1 in type_select
    assert option_2 in type_select

    # Confirm proper select tags are present
    select_regex = re.compile(r'^<select class=\"dictionary-type\">.*<\/select>$')
    assert select_regex.match(type_select)


def test__generate_select_data__dictionary_class_details():
    """Confirms response returns expected dictionary class details."""
    # Create test languages
    class_1 = models.DictionaryClass.objects.create(
        class_name='1',
        class_verbose_name='One',
    )
    class_2 = models.DictionaryClass.objects.create(
        class_name='2',
        class_verbose_name='Two',
    )

    selects = views.generate_select_data()
    class_select = selects['dict_class']

    # Confirm options are present as expected
    option_1 = f'<option value="{class_1.id}">{class_1.class_name}</option>'
    option_2 = f'<option value="{class_2.id}">{class_2.class_name}</option>'

    assert option_1 in class_select
    assert option_2 in class_select

    # Confirm proper select tags are present
    select_regex = re.compile(r'^<select class=\"dictionary-class\">.*<\/select>$')
    assert select_regex.match(class_select)


def test__review__200_response():
    """Confirms review view returns 200 response."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.META = {}  # Need to add this attribute for view to load
    response = views.review(request)

    # Confirm status code
    assert response.status_code == 200

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__review__template(user):
    """Confirms review view returns expected template.

        Need to load permissions properly here to get full response
        context.
    """
    # Add user permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Get response
    response = client.get(reverse('dictionary_review'))

    assert (
        'dictionary/review.html' in [t.name for t in response.templates]
    )


def test__review__context(user, dictionary_word_pending):  # pylint: disable=unused-argument
    """Confirms review view returns expected context details.

        Need to load permissions properly here to get full response
        context.
    """
    # Add user permissions
    utils.add_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user)

    # Get response
    response = client.get(reverse('dictionary_review'))

    # Test for context key
    assert 'count' in response.context

    # Confirm proper count
    assert response.context['count'] == models.WordPending.objects.all().count()


def test__retrieve_entries__200_response():
    """Confirms retrieve entries view returns 200 response."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'last_id': 1, 'request_num': 1}
    response = views.retrieve_entries(request)

    # Confirm status code
    assert response.status_code == 200

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__retrieve_entries__missing_last_id():
    """Confirms retrieve entries view returns 400 response on missing last_id."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'request_num': 1}
    response = views.retrieve_entries(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm message details
    json_response = json.loads(response.content)

    assert 'status_code' in json_response
    assert 'success' in json_response
    assert 'errors' in json_response

    assert json_response['status_code'] == 400
    assert json_response['success'] is False
    assert json_response['errors'] == ['"last_id" and "request_num" are a required parameters.']

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__retrieve_entries__missing_request_num():
    """Confirms retrieve entries view returns 400 response on missing request_num."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {'last_id': 1}
    response = views.retrieve_entries(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm message details
    json_response = json.loads(response.content)

    assert 'status_code' in json_response
    assert 'success' in json_response
    assert 'errors' in json_response

    assert json_response['status_code'] == 400
    assert json_response['success'] is False
    assert json_response['errors'] == ['"last_id" and "request_num" are a required parameters.']

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__retrieve_entries__405_response():
    """Confirms retrieve entries view returns 405 response on non-POST."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'GET'
    request.POST = {'last_id': 1, 'request_num': 1}
    response = views.retrieve_entries(request)

    # Confirm status code
    assert response.status_code == 405

    # Confirm message details
    json_response = json.loads(response.content)

    assert 'status_code' in json_response
    assert 'success' in json_response
    assert 'errors' in json_response

    assert json_response['status_code'] == 405
    assert json_response['success'] is False
    assert json_response['errors'] == ['Only "POST" method is allowed.']

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__retrieve_pending_entries__confirm_response_details(dictionary_word_pending):
    """Confirms response type and details."""
    # References for word creation
    language = dictionary_word_pending.language
    dictionary_type = dictionary_word_pending.dictionary_type
    dictionary_class = dictionary_word_pending.dictionary_class

    # Delete any existing words
    models.WordPending.objects.all().delete()

    # Create new words for testing
    word_1 = models.WordPending.objects.create(
        language=language,
        dictionary_type=dictionary_type,
        dictionary_class=dictionary_class,
        original_words='Original Word 1',
        word='One',
    )
    word_2 = models.WordPending.objects.create(
        language=language,
        dictionary_type=dictionary_type,
        dictionary_class=dictionary_class,
        original_words='Original Word 2',
        word='Two',
    )

    # Request all entries for testing
    pending_count = models.WordPending.objects.all().count()
    response = views.retrieve_pending_entries(0, pending_count)

    # Confirm type of response
    assert isinstance(response, dict)

    # Confirm keys and their types
    assert 'status_code' in response
    assert isinstance(response['status_code'], int)
    assert 'content' in response
    assert isinstance(response['content'], list)

    # Confirm response values
    assert response['status_code'] == 200
    assert len(response['content']) == pending_count
    assert response['content'][0]['id'] == word_1.pk
    assert response['content'][0]['word'] == word_1.word
    assert response['content'][0]['original'] == word_1.original_words
    assert response['content'][0]['language'] == word_1.language.id
    assert response['content'][0]['dictionary_type'] == word_1.dictionary_type.id
    assert response['content'][0]['dictionary_class'] == word_1.dictionary_class.id
    assert response['content'][1]['id'] == word_2.pk


def test__retrieve_pending_entries__confirm_query_results(dictionary_word_pending):
    """Confirms query results return expected values."""
    # References for word creation
    language = dictionary_word_pending.language
    dictionary_type = dictionary_word_pending.dictionary_type
    dictionary_class = dictionary_word_pending.dictionary_class

    # Delete any existing words
    models.WordPending.objects.all().delete()

    # Create new words for testing
    word_1 = models.WordPending.objects.create(
        language=language,
        dictionary_type=dictionary_type,
        dictionary_class=dictionary_class,
        original_words='Original Word 1',
        word='One',
    )
    models.WordPending.objects.create(
        language=language,
        dictionary_type=dictionary_type,
        dictionary_class=dictionary_class,
        original_words='Original Word 2',
        word='Two',
    )


    # Request only the first entry
    response = views.retrieve_pending_entries(0, 1)

    # Confirm only first item returned
    assert len(response['content']) == 1
    assert response['content'][0]['id'] == word_1.pk


def test__add_new_word__201_response(dictionary_word_pending):
    """Confirms add new word view returns 201 response."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {
        'pending_id': dictionary_word_pending.pk,
        'model_name': 'word',
        'word': 'abc',
        'language': dictionary_word_pending.language.pk,
        'dictionary_type': dictionary_word_pending.dictionary_type.pk,
        'dictionary_class': dictionary_word_pending.dictionary_class.pk,
    }
    response = views.add_new_word(request)

    # Confirm status code
    assert response.status_code == 201

    # Confirm message details added as part of view
    json_response = json.loads(response.content)

    assert 'id' in json_response
    assert json_response['id'] == dictionary_word_pending.pk

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__add_new_word__missing_pending_id(dictionary_word_pending):
    """Confirms add new word returns 400 response on missing pending_id."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {
        'model_name': 'word',
        'word': 'abc',
        'language': dictionary_word_pending.language.pk,
        'dictionary_type': dictionary_word_pending.dictionary_type.pk,
        'dictionary_class': dictionary_word_pending.dictionary_class.pk,
    }
    response = views.add_new_word(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm message details
    json_response = json.loads(response.content)

    assert 'status_code' in json_response
    assert 'success' in json_response
    assert 'errors' in json_response

    assert json_response['status_code'] == 400
    assert json_response['success'] is False
    assert json_response['errors'] == ['POST request missing arguments: pending_id']

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__add_new_word__missing_model_name(dictionary_word_pending):
    """Confirms add new word returns 400 response on missing model_name."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {
        'pending_id': dictionary_word_pending.pk,
        'word': 'abc',
        'language': dictionary_word_pending.language.pk,
        'dictionary_type': dictionary_word_pending.dictionary_type.pk,
        'dictionary_class': dictionary_word_pending.dictionary_class.pk,
    }
    response = views.add_new_word(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm message details
    json_response = json.loads(response.content)

    assert 'status_code' in json_response
    assert 'success' in json_response
    assert 'errors' in json_response

    assert json_response['status_code'] == 400
    assert json_response['success'] is False
    assert json_response['errors'] == ['POST request missing arguments: model_name']

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__add_new_word__missing_word(dictionary_word_pending):
    """Confirms add new word returns 400 response on missing word."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {
        'pending_id': dictionary_word_pending.pk,
        'model_name': 'word',
        'language': dictionary_word_pending.language.pk,
        'dictionary_type': dictionary_word_pending.dictionary_type.pk,
        'dictionary_class': dictionary_word_pending.dictionary_class.pk,
    }
    response = views.add_new_word(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm message details
    json_response = json.loads(response.content)

    assert 'status_code' in json_response
    assert 'success' in json_response
    assert 'errors' in json_response

    assert json_response['status_code'] == 400
    assert json_response['success'] is False
    assert json_response['errors'] == ['POST request missing arguments: word']

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__add_new_word__missing_language(dictionary_word_pending):
    """Confirms add new word returns 400 response on missing language."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {
        'pending_id': dictionary_word_pending.pk,
        'model_name': 'word',
        'word': 'abc',
        'dictionary_type': dictionary_word_pending.dictionary_type.pk,
        'dictionary_class': dictionary_word_pending.dictionary_class.pk,
    }
    response = views.add_new_word(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm message details
    json_response = json.loads(response.content)

    assert 'status_code' in json_response
    assert 'success' in json_response
    assert 'errors' in json_response

    assert json_response['status_code'] == 400
    assert json_response['success'] is False
    assert json_response['errors'] == ['POST request missing arguments: language']

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__add_new_word__missing_dictionary_type(dictionary_word_pending):
    """Confirms add new word returns 400 response on missing dictionary_type."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {
        'pending_id': dictionary_word_pending.pk,
        'model_name': 'word',
        'word': 'abc',
        'language': dictionary_word_pending.language.pk,
        'dictionary_class': dictionary_word_pending.dictionary_class.pk,
    }
    response = views.add_new_word(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm message details
    json_response = json.loads(response.content)

    assert 'status_code' in json_response
    assert 'success' in json_response
    assert 'errors' in json_response

    assert json_response['status_code'] == 400
    assert json_response['success'] is False
    assert json_response['errors'] == ['POST request missing arguments: dictionary_type']

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__add_new_word__missing_dictionary_class(dictionary_word_pending):
    """Confirms add new word returns 400 response on missing dictionary_class."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {
        'pending_id': dictionary_word_pending.pk,
        'model_name': 'word',
        'word': 'abc',
        'language': dictionary_word_pending.language.pk,
        'dictionary_type': dictionary_word_pending.dictionary_type.pk,
    }
    response = views.add_new_word(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm message details
    json_response = json.loads(response.content)

    assert 'status_code' in json_response
    assert 'success' in json_response
    assert 'errors' in json_response

    assert json_response['status_code'] == 400
    assert json_response['success'] is False
    assert json_response['errors'] == ['POST request missing arguments: dictionary_class']

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__add_new_word__405_response(dictionary_word_pending):
    """Confirms add new word view returns 405 response on non-POST."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'GET'
    request.POST = {
        'pending_id': dictionary_word_pending.pk,
        'model_name': 'word',
        'word': 'abc',
        'language': dictionary_word_pending.language.pk,
        'dictionary_type': dictionary_word_pending.dictionary_type.pk,
        'dictionary_class': dictionary_word_pending.dictionary_class.pk,
    }
    response = views.add_new_word(request)

    # Confirm status code
    assert response.status_code == 405

    # Confirm message details
    json_response = json.loads(response.content)

    assert 'status_code' in json_response
    assert 'success' in json_response
    assert 'errors' in json_response

    assert json_response['status_code'] == 405
    assert json_response['success'] is False
    assert json_response['errors'] == ['Only "POST" method is allowed.']

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__process_new_word__confirm_response_word(dictionary_word_pending):
    """Confirms response type and details for a new Word."""
    response = views.process_new_word(
        'word',
        '1',
        dictionary_word_pending.language.pk,
        dictionary_word_pending.dictionary_type.pk,
        dictionary_word_pending.dictionary_class.pk,
    )

    # Confirm response type
    assert isinstance(response, dict)

    # Confirm response keys and types
    assert 'status_code' in response
    assert isinstance(response['status_code'], int)
    assert 'success' in response
    assert isinstance(response['success'], bool)
    assert 'message' in response
    assert isinstance(response['message'], str)
    assert 'id' in response
    assert isinstance(response['id'], int)

    # Confirm response details
    assert response['status_code'] == 201
    assert response['success'] is True
    assert response['message'] == '1 added to the Word dictionary'


def test__process_new_word__confirm_response_excluded(dictionary_word_pending):
    """Confirms response details for ExcludedWord."""
    response = views.process_new_word(
        'excluded',
        '1',
        dictionary_word_pending.language.pk,
        dictionary_word_pending.dictionary_type.pk,
        dictionary_word_pending.dictionary_class.pk,
    )

    # Confirm response details
    assert response['message'] == '1 added to the Excluded Word dictionary'


def test__process_new_word__confirm_word_creation(dictionary_word_pending):
    """Confirms that function creates word as expected."""
    # Get current model counts
    word_count = models.Word.objects.all().count()
    excluded_count = models.ExcludedWord.objects.all().count()

    views.process_new_word(
        'word',
        '1',
        dictionary_word_pending.language.pk,
        dictionary_word_pending.dictionary_type.pk,
        dictionary_word_pending.dictionary_class.pk,
    )

    # Confirm model creation
    assert models.Word.objects.all().count() == word_count + 1
    assert models.ExcludedWord.objects.all().count() == excluded_count


def test__process_new_word__confirm_excluded_word_creation(dictionary_word_pending):
    """Confirms that function creates ExcludedWord as expected."""
    # Get current model counts
    word_count = models.Word.objects.all().count()
    excluded_count = models.ExcludedWord.objects.all().count()

    views.process_new_word(
        'excluded',
        '1',
        dictionary_word_pending.language.pk,
        dictionary_word_pending.dictionary_type.pk,
        dictionary_word_pending.dictionary_class.pk,
    )

    # Confirm model creation
    assert models.Word.objects.all().count() == word_count
    assert models.ExcludedWord.objects.all().count() == excluded_count + 1


def test__delete_pending_word__204_response(dictionary_word_pending):
    """Confirms add new word view returns 204 response."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {
        'pending_id': dictionary_word_pending.pk,
    }
    response = views.delete_pending_word(request)

    # Confirm status code
    assert response.status_code == 204

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__delete_pending_word__missing_pending_id():
    """Confirms add new word returns 400 response on missing pending_id."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {}
    response = views.delete_pending_word(request)

    # Confirm status code
    assert response.status_code == 400

    # Confirm message details
    json_response = json.loads(response.content)

    assert 'status_code' in json_response
    assert 'success' in json_response
    assert 'errors' in json_response

    assert json_response['status_code'] == 400
    assert json_response['success'] is False
    assert json_response['errors'] == ['POST request missing pending ID']

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__delete_pending_word__405_response(dictionary_word_pending):
    """Confirms delete pending word view returns 405 response on non-POST."""
    # Start permission patch
    permission_patch.start()
    importlib.reload(views)

    # Create request, view, and response
    request = RequestFactory()
    request.method = 'GET'
    request.POST = {
        'pending_id': dictionary_word_pending.pk,
    }
    response = views.delete_pending_word(request)

    # Confirm status code
    assert response.status_code == 405

    # Confirm message details
    json_response = json.loads(response.content)

    assert 'status_code' in json_response
    assert 'success' in json_response
    assert 'errors' in json_response

    assert json_response['status_code'] == 405
    assert json_response['success'] is False
    assert json_response['errors'] == ['Only "POST" method is allowed.']

    # Stop permission patch
    permission_patch.stop()
    importlib.reload(views)


def test__process_pending_word_deletion__confirm_response(dictionary_word_pending):
    """Confirms response type & details of processing_pending_word_deletion."""
    pending_pk = dictionary_word_pending.pk
    response = views.process_pending_word_deletion(pending_pk)

    # Confirm response type
    assert isinstance(response, dict)

    # Confirm keys and types
    assert 'id' in response
    assert isinstance(response['id'], int)
    assert 'success' in response
    assert isinstance(response['success'], bool)
    assert 'status_code' in response
    assert isinstance(response['status_code'], int)
    assert 'message' in response
    assert isinstance(response['message'], str)

    # Confirm response values
    assert response['id'] == pending_pk
    assert response['success'] is True
    assert response['status_code'] == 204
    assert response['message'] == f'Pending word (id = {pending_pk}) successfully deleted'


def test__process_pending_word_deletion__confirm_deletion(dictionary_word_pending):
    """Confirms pending word is deleted as expected."""
    pending_pk = dictionary_word_pending.pk
    views.process_pending_word_deletion(pending_pk)

    assert models.WordPending.objects.filter(pk=pending_pk).exists() is False
