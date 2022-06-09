"""Tests for the HC DPD API URLs."""
import pytest

from django.urls import reverse

from rest_framework.test import APIClient

from api.hc_dpd.tests import utils
from users.tests.utils import create_token


pytestmark = pytest.mark.django_db


def test__upload_hc_dpd_data__401_response_on_anonymous_user():
    """Test for 403 response on anonymous user."""
    # Set up client and response
    client = APIClient()
    response = client.post(
        reverse('api:hc_dpd_v1:upload_hc_dpd_data'),
        data={'active_ingredient': [{'drug_code': 1, 'active_ingredient_code': 'A'}]},
        format='json',
    )

    assert response.status_code == 401  # pylint: disable=no-member


def test__upload_hc_dpd_data__403_response_on_user_without_permissions(user):
    """Test for 403 response on user without permission."""
    # Create token
    token = create_token(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse('api:hc_dpd_v1:upload_hc_dpd_data'),
        data={'active_ingredient': [{'drug_code': 1, 'active_ingredient_code': 'A'}]},
        format='json',
    )

    assert response.status_code == 403


def test__upload_hc_dpd_data__403_response_on_user_with_view_permissions(user):
    """Test for 403 response on user with view permission."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_view_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse('api:hc_dpd_v1:upload_hc_dpd_data'),
        data={'active_ingredient': [{'drug_code': 1, 'active_ingredient_code': 'A'}]},
        format='json',
    )

    assert response.status_code == 403


def test__upload_hc_dpd_data__201_response_on_user_with_edit_permissions(user):
    """Test for 201 response on user with view permission."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_edit_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse('api:hc_dpd_v1:upload_hc_dpd_data'),
        data={'active_ingredient': [{'drug_code': 1, 'active_ingredient_code': 'A'}]},
        format='json',
    )

    assert response.status_code == 201


def test__upload_hc_dpd_data__accessible_by_url(user):
    """Tests that endpoint exists at expected URL."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_edit_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        '/api/hc-dpd/v1/upload/',
        {'active_ingredient': [{'drug_code': 1, 'active_ingredient_code': 'A'}]},
        format='json',
    )

    assert response.status_code == 201


def test__checksum_list__401_response_on_anonymous_user():
    """Test for 403 response on anonymous user."""
    # Set up client and response
    client = APIClient()
    response = client.get(
        reverse('api:hc_dpd_v1:checksum_list'),
        data={'step': 1, 'source': 'active_ingredient'},
    )

    assert response.status_code == 401


def test__checksum_list__403_response_on_user_without_permissions(user):
    """Test for 403 response on user without permission."""
    # Create token
    token = create_token(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(
        reverse('api:hc_dpd_v1:checksum_list'),
        data={'step': 1, 'source': 'active_ingredient'},
    )

    assert response.status_code == 403


def test__checksum_list__200_response_on_user_with_view_permissions(user):
    """Test for 200 response on user with view permission."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_view_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(
        reverse('api:hc_dpd_v1:checksum_list'),
        data={'step': 1, 'source': 'active_ingredient'},
    )

    assert response.status_code == 200


def test__checksum_list__200_response_on_user_with_edit_permissions(user):
    """Test for 200 response on user with view permission."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_edit_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(
        reverse('api:hc_dpd_v1:checksum_list'),
        data={'step': 1, 'source': 'active_ingredient'},
    )

    assert response.status_code == 200


def test__checksum_list__accessible_by_url(user):
    """Tests that endpoint exists at expected URL."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_view_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get('/api/hc-dpd/v1/checksum/?step=1&source=active_ingredient')

    assert response.status_code == 200


def test__checksum_test__403_response_on_user_without_permissions(user):
    """Test for 403 response on user without permission."""
    # Create token
    token = create_token(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse('api:hc_dpd_v1:checksum_test'),
        data={'active_ingredient': [{'drug_code': 1, 'active_ingredient_code': 'A'}]},
        format='json',
    )

    assert response.status_code == 403


def test__checksum_test__200_response_on_user_with_view_permissions(user):
    """Test for 200 response on user with view permission."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_view_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse('api:hc_dpd_v1:checksum_test'),
        data={'active_ingredient': [{'drug_code': 1, 'active_ingredient_code': 'A'}]},
        format='json',
    )

    assert response.status_code == 200


def test__checksum_test__200_response_on_user_with_edit_permissions(user):
    """Test for 201 response on user with view permission."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_edit_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse('api:hc_dpd_v1:checksum_test'),
        data={'active_ingredient': [{'drug_code': 1, 'active_ingredient_code': 'A'}]},
        format='json',
    )

    assert response.status_code == 200


def test__checksum_test__accessible_by_url(user):
    """Tests that endpoint exists at expected URL."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_edit_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        '/api/hc-dpd/v1/checksum/test/',
        {'active_ingredient': [{'drug_code': 1, 'active_ingredient_code': 'A'}]},
        format='json',
    )

    assert response.status_code == 200
