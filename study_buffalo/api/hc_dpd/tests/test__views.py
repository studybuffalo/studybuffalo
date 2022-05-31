"""Tests for the HC DPD API views."""
# pylint: disable=protected-access
import json
from unittest.mock import patch

import pytest

from django.test import RequestFactory
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError
from api.hc_dpd.tests import utils
from api.hc_dpd import views
from hc_dpd import models
from users.tests.utils import create_token


pytestmark = pytest.mark.django_db


def test__upload_hc_dpd_data__valid_post(user):
    """Tests that proper response is returned."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_edit_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse('api:hc_dpd_v1:upload_hc_dpd_data'),
        data=utils.UPLOAD_ALL_DATA,
        format='json',
    )
    content = json.loads(response.content)

    # Confirm status code
    assert response.status_code == 201

    # Confirm response details are received as expected
    assert 'message' in content
    assert isinstance(content['message'], list)
    assert len(content['message']) == 13

    assert 'status_code' in content
    assert content['status_code'] == 201


def test__upload_hc_dpd_data__invalid_post__data_errors(user):
    """Tests that proper response is returned for invalid post data."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_edit_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse('api:hc_dpd_v1:upload_hc_dpd_data'),
        data={'active_ingredient': [{'drug_code': 'ERROR'}]},
        format='json',
    )
    content = json.loads(response.content)

    # Confirm status code
    assert response.status_code == 400

    # Confirm response details are received as expected
    assert 'errors' in content
    assert isinstance(content['errors'], dict)
    assert 'non_field' in content['errors']
    assert isinstance(content['errors']['non_field'], list)
    assert 'field' in content['errors']
    assert isinstance(content['errors']['field'], dict)

    assert 'status_code' in content
    assert content['status_code'] == 400


def test__upload_hc_dpd_data__invalid_post___no_data(user):
    """Tests that proper response is returned for no post data."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_edit_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse('api:hc_dpd_v1:upload_hc_dpd_data'),
        data={},
        format='json',
    )
    content = json.loads(response.content)

    # Confirm status code
    assert response.status_code == 400

    # Confirm response details are received as expected
    assert 'errors' in content
    assert isinstance(content['errors'], dict)
    assert 'non_field' in content['errors']
    assert isinstance(content['errors']['non_field'], list)
    assert content['errors']['non_field'] == ['No data submitted for upload.']
    assert 'field' in content['errors']
    assert isinstance(content['errors']['field'], dict)

    assert 'status_code' in content
    assert content['status_code'] == 400


def test__upload_hc_dpd_data__invalid_method(user):
    """Tests that proper response is returned for invalid method (GET)."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_edit_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(
        reverse('api:hc_dpd_v1:upload_hc_dpd_data'),
        data=utils.UPLOAD_ALL_DATA,
        format='json',
    )
    content = json.loads(response.content)

    # Confirm status code
    assert response.status_code == 405

    # Confirm message
    assert content == {'detail': 'Method "GET" not allowed.'}


@patch('api.hc_dpd.views.ChecksumList._get_validated_parameters')
def test__checksum_list__get_queryset(parameters):
    """Confirms proper queryset is returned."""
    # Create DPDChecksum instances for testing
    for i in range(1, 101):
        models.DPDChecksum.objects.create(
            drug_code_start=i,
            drug_code_step=1,
            extract_source='active_ingredient',
            checksum=i,
        )

    # Get view instance
    view = views.ChecksumList()

    # Mock the parameter details
    parameters.return_value = {'step': 1, 'source': 'active_ingredient'}

    queryset = view.get_queryset()

    # Confirm proper number of results in query
    assert queryset.count() == 100

    # Confirm details of query items
    first_item = queryset.get(drug_code_start=1)
    assert first_item == models.DPDChecksum.objects.get(drug_code_start=1)


def test__checksum_list__get_validated_parameters__valid_data():
    """Confirms validated data is returned with correct parameters."""
    # Get view instance
    view = views.ChecksumList()
    request = RequestFactory()
    request.query_params = {'step': 1, 'source': 'active_ingredient'}
    view.request = request

    # Get the validated parameters
    parameters = view._get_validated_parameters()

    assert parameters == {'step': 1, 'source': 'active_ingredient'}


def test__checksum_list__get_validated_parameters__invalid_data():
    """Confirms exception raised when invalid parameters provided."""
    # Get view instance
    view = views.ChecksumList()
    request = RequestFactory()
    request.query_params = {'step': 1, 'source': 'A'}
    view.request = request

    # Get the validated parameters
    try:
        view._get_validated_parameters()
    except ValidationError as error:
        assert error.status_code == 400
        assert 'source' in error.detail
        assert '"A" is not a valid choice.' in str(error.detail['source'][0])
    else:
        assert False


def test__checksum_list__valid_data(user, hc_dpd_checksum_active_ingredient):
    """Tests proper response is returned for valid data."""
    checksum = hc_dpd_checksum_active_ingredient

    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_edit_permission(user)

    # Set up client and response
    data = {'step': checksum.drug_code_step, 'source': checksum.extract_source}
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(
        reverse('api:hc_dpd_v1:checksum_list'),
        data=data,
        format='json',
    )
    content = json.loads(response.content)

    # Confirm status code
    assert response.status_code == 200

    # Confirm response details
    assert 'count' in content
    assert content['count'] == 1
    assert 'next' in content
    assert content['next'] is None
    assert 'previous' in content
    assert content['previous'] is None
    assert 'results' in content
    assert content['results'] == [{
        'drug_code_start': checksum.drug_code_start,
        'drug_code_step': checksum.drug_code_step,
        'extract_source': checksum.extract_source,
        'checksum': str(checksum.checksum),
        'checksum_date': checksum.checksum_date.strftime('%Y-%m-%d'),
    }]


def test__checksum_list__invalid_data(user):
    """Tests proper response is returned for invalid data."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_edit_permission(user)

    # Set up client and response
    data = {'step': 0, 'source': 'active_ingredient'}
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(
        reverse('api:hc_dpd_v1:checksum_list'),
        data=data,
        format='json',
    )
    content = json.loads(response.content)

    # Confirm status code
    assert response.status_code == 400

    # Confirm response details
    assert content == {'step': ['"0" is not a valid choice.']}


def test__checksum_list__pagination(user):
    """Test for proper details for paginated response."""
    # Create enough DPDChecksum instances for testing
    for i in range(1, 2001):
        models.DPDChecksum.objects.create(
            drug_code_start=i,
            drug_code_step=1,
            extract_source='active_ingredient',
            checksum=i,
        )

    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_edit_permission(user)

    # Set up client and response
    data = {'step': 1, 'source': 'active_ingredient'}
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(
        reverse('api:hc_dpd_v1:checksum_list'),
        data=data,
        format='json',
    )
    content = json.loads(response.content)

    # Confirm status code
    assert response.status_code == 200

    # Confirm response details
    assert 'count' in content
    assert content['count'] == 2000
    assert 'next' in content
    assert '/api/hc-dpd/v1/checksum/?page=2&source=active_ingredient&step=1' in content['next']
    assert 'previous' in content
    assert content['previous'] is None
    assert 'results' in content
    assert isinstance(content['results'], list)
    assert len(content['results']) == 1000


def test__checksum_list__invalid_method(user):
    """Tests that proper response is returned for invalid method (POST)."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_edit_permission(user)

    # Set up client and response
    data = {'step': 1, 'source': 'active_ingredient'}
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse('api:hc_dpd_v1:checksum_list'),
        data=data,
        format='json',
    )
    content = json.loads(response.content)

    # Confirm status code
    assert response.status_code == 405

    # Confirm message
    assert content == {'detail': 'Method "POST" not allowed.'}


def test__checksum_test__valid_data(user):
    """Tests proper response is returned for valid data."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_view_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse('api:hc_dpd_v1:checksum_test'),
        data=utils.UPLOAD_ALL_DATA,
        format='json',
    )
    content = json.loads(response.content)

    # Confirm status code
    assert response.status_code == 200

    # Confirm response details
    assert len(content) == 13
    assert 'active_ingredient' in content
    assert 'server_checksum' in content['active_ingredient']
    assert len(str(content['active_ingredient']['server_checksum'])) == 10
    assert 'server_checksum_string' in content['active_ingredient']
    assert content['active_ingredient']['server_checksum_string'] == '1ABCDEFGHIJKLMN'
    assert 'active_ingredient' in content
    assert 'biosimilar' in content
    assert 'company' in content
    assert 'drug_product' in content
    assert 'form' in content
    assert 'inactive_product' in content
    assert 'packaging' in content
    assert 'pharmaceutical_standard' in content
    assert 'schedule' in content
    assert 'status' in content
    assert 'therapeutic_class' in content
    assert 'veterinary_species' in content


def test__checksum_test__invalid_data(user):
    """Tests proper response is returned for invalid data."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_view_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse('api:hc_dpd_v1:checksum_test'),
        data={'active_ingredient': [{'drug_code': 'ERROR'}]},
        format='json',
    )
    content = json.loads(response.content)

    # Confirm status code
    assert response.status_code == 400
    assert content['status_code'] == 400

    # Confirm response details
    assert 'errors' in content
    assert len(content['errors']) > 0


def test__checksum_test__invalid_method(user):
    """Tests that proper response is returned for invalid method (GET)."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_edit_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(
        reverse('api:hc_dpd_v1:checksum_test'),
        data=utils.UPLOAD_ALL_DATA,
        format='json',
    )

    content = json.loads(response.content)

    # Confirm status code
    assert response.status_code == 405

    # Confirm message
    assert content == {'detail': 'Method "GET" not allowed.'}
