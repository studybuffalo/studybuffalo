"""Tests for the RDRHC Calendar API URLs."""
import pytest

from django.urls import reverse

from rest_framework.test import APIClient

from rdrhc_calendar.models import CalendarUser
from rdrhc_calendar.tests import utils


pytestmark = pytest.mark.django_db

def test__root__403_response_on_anonymous_user():
    """Test for 403 response on anonymous user."""
    # Set up client and response
    client = APIClient()
    response = client.get(reverse('rdrhc_calendar:api_v1:root'))

    assert response.status_code == 403

def test__root__403_response_on_user_without_permissions(user):
    """Test for 403 response on user without permission."""
    # Create token
    token = utils.create_token(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse('rdrhc_calendar:api_v1:root'))

    assert response.status_code == 403

def test__root__200_response_on_user_with_permissions(user):
    """Test for 200 response on user with permission."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse('rdrhc_calendar:api_v1:root'))

    assert response.status_code == 200

def test__root__accessible_by_url(user):
    """Tests that endpoint exists at expected URL."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get('/rdrhc-calendar/api/v1/')

    assert response.status_code == 200

def test__user_list__403_response_on_anonymous_user():
    """Test for 403 response on anonymous user."""
    # Set up client and response
    client = APIClient()
    response = client.get(reverse('rdrhc_calendar:api_v1:user_list'))

    assert response.status_code == 403

def test__user_list__403_response_on_user_without_permissions(user):
    """Test for 403 response on user without permission."""
    # Create token
    token = utils.create_token(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse('rdrhc_calendar:api_v1:user_list'))

    assert response.status_code == 403

def test__user_list__200_response_on_user_with_permissions(user):
    """Test for 200 response on user with permission."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Add permission to user
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse('rdrhc_calendar:api_v1:user_list'))

    assert response.status_code == 200

def test__user_list__accessible_by_url(user):
    """Tests that endpoint exists at expected URL."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get('/rdrhc-calendar/api/v1/users/')

    assert response.status_code == 200

def test__user_detail__403_response_on_anonymous_user(user):
    """Test for 403 response on anonymous user."""
    # Set up client and response
    client = APIClient()
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_detail', kwargs={'user_id': user.id}
    ))

    assert response.status_code == 403

def test__user_detail__403_response_on_user_without_permissions(calendar_user):
    """Test for 403 response on user without permission."""
    # Create token
    token = utils.create_token(calendar_user.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_detail', kwargs={'user_id': calendar_user.id}
    ))

    assert response.status_code == 403

def test__user_detail__200_response_on_user_with_permissions(calendar_user):
    """Test for 200 response on user with permission."""
    # Create token and add user permissions
    token = utils.create_token(calendar_user.sb_user)
    utils.add_api_permission(calendar_user.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_detail',
        kwargs={'user_id': calendar_user.id}
    ))

    assert response.status_code == 200

def test__user_detail__accessible_by_url(calendar_user):
    """Tests that endpoint exists at expected URL."""
    # Create token and add user permissions
    token = utils.create_token(calendar_user.sb_user)
    utils.add_api_permission(calendar_user.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(
        '/rdrhc-calendar/api/v1/users/{}/'.format(calendar_user.id)
    )

    assert response.status_code == 200

def test__user_email_list__403_response_on_anonymous_user(user):
    """Test for 403 response on anonymous user."""
    # Set up client and response
    client = APIClient()
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_email_list', kwargs={'user_id': user.id}
    ))

    assert response.status_code == 403

def test__user_email_list__403_response_on_user_without_permissions(user):
    """Test for 403 response on user without permission."""
    # Create token
    token = utils.create_token(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_email_list', kwargs={'user_id': token.user.id}
    ))

    assert response.status_code == 403

def test__user_email_list__200_response_on_user_with_permissions(user):
    """Test for 200 response on user with permission."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_email_list',
        kwargs={'user_id': token.user.id}
    ))

    assert response.status_code == 200

def test__user_email_list__accessible_by_url(user):
    """Tests that endpoint exists at expected URL."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(
        '/rdrhc-calendar/api/v1/users/{}/emails/'.format(token.user.id)
    )

    assert response.status_code == 200

def test__shift_list__403_response_on_anonymous_user():
    """Test for 403 response on anonymous user."""
    # Set up client and response
    client = APIClient()
    response = client.get(reverse('rdrhc_calendar:api_v1:shift_list'))

    assert response.status_code == 403

def test__shift_list__403_response_on_user_without_permissions(user):
    """Test for 403 response on user without permission."""
    # Create token and add user permissions
    token = utils.create_token(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse('rdrhc_calendar:api_v1:shift_list'))

    assert response.status_code == 403

def test__shift_list__200_response_on_user_with_permissions(user):
    """Test for 200 response on user with permission."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse('rdrhc_calendar:api_v1:shift_list'))

    assert response.status_code == 200

def test__shift_list__accessible_by_url(user):
    """Tests that endpoint exists at expected URL."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get('/rdrhc-calendar/api/v1/shifts/')

    assert response.status_code == 200

def test__user_shift_code_list__403_response_on_anonymous_user(user):
    """Test for 403 response on anonymous user."""
    # Set up client and response
    client = APIClient()
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_shift_codes_list',
        kwargs={'user_id': user.id}
    ))

    assert response.status_code == 403

def test__user_shift_code_list__403_response_on_user_without_permissions(calendar_user):
    """Test for 403 response on user without permission."""
    # Create token
    token = utils.create_token(calendar_user.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_email_list', kwargs={'user_id': token.user.id}
    ))

    assert response.status_code == 403

def test__user_shift_code_list__200_response_on_user_with_permissions(calendar_user):
    """Test for 200 response on user with permission."""
    # Create token and add user permissions
    token = utils.create_token(calendar_user.sb_user)
    utils.add_api_permission(calendar_user.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_shift_codes_list',
        kwargs={'user_id': token.user.id}
    ))

    assert response.status_code == 200

def test__user_shift_code_list__accessible_by_url(calendar_user):
    """Tests that endpoint exists at expected URL."""
    # Create token and add user permissions
    token = utils.create_token(calendar_user.sb_user)
    utils.add_api_permission(calendar_user.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(
        '/rdrhc-calendar/api/v1/shift-codes/{}/'.format(token.user.id)
    )

    assert response.status_code == 200

def test__stat_holiday_list__403_response_on_anonymous_user():
    """Test for 403 response on anonymous user."""
    # Set up client and response
    client = APIClient()
    response = client.get(reverse('rdrhc_calendar:api_v1:stat_holidays_list'))

    assert response.status_code == 403

def test__stat_holiday_list__403_response_on_user_without_permissions(user):
    """Test for 403 response on user without permission."""
    # Create token and add user permissions
    token = utils.create_token(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:stat_holidays_list'
    ))

    assert response.status_code == 403

def test__stat_holiday_list__200_response_on_user_with_permissions(user):
    """Test for 200 response on user with permission."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse('rdrhc_calendar:api_v1:stat_holidays_list'))

    assert response.status_code == 200

def test__stat_holiday_list__accessible_by_url(user):
    """Tests that endpoint exists at expected URL."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get('/rdrhc-calendar/api/v1/stat-holidays/')

    assert response.status_code == 200

def test__user_schedule_list__403_response_on_anonymous_user(user):
    """Test for 403 response on anonymous user."""
    # Set up client and response
    client = APIClient()
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_schedule_list', kwargs={'user_id': user.id}
    ))
    assert response.status_code == 403

def test__user_schedule_list__403_response_on_user_without_permissions(user):
    """Test for 403 response on user without permission."""
    # Create token and add user permissions
    token = utils.create_token(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_schedule_list', kwargs={'user_id': token.user.id}
    ))

    assert response.status_code == 403

def test__user_schedule_list__200_response_on_user_with_permissions(user):
    """Test for 200 response on user with permission."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_schedule_list',
        kwargs={'user_id': token.user.id}
    ))

    assert response.status_code == 200

def test__user_schedule_list__accessible_by_url(user):
    """Tests that endpoint exists at expected URL."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(
        '/rdrhc-calendar/api/v1/shifts/{}/'.format(token.user.id)
    )

    assert response.status_code == 200

def test__user_schedule_delete__403_response_on_anonymous_user(user):
    """Test for 403 response on anonymous user."""
    # Set up client and response
    client = APIClient()
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_schedule_delete',
        kwargs={'user_id': user.id}
    ))

    assert response.status_code == 403

def test__user_schedule_delete__403_response_on_user_without_permissions(user):
    """Test for 403 response on user without permission."""
    # Create token and add user permissions
    token = utils.create_token(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_schedule_delete', kwargs={'user_id': token.user.id}
    ))

    assert response.status_code == 403

def test__user_schedule_delete__204_response_on_user_with_permissions(user):
    """Test for 200 response on user with permission."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.delete(reverse(
        'rdrhc_calendar:api_v1:user_schedule_delete',
        kwargs={'user_id': token.user.id}
    ))

    assert response.status_code == 204

def test__user_schedule_delete__accessible_by_url(user):
    """Tests that endpoint exists at expected URL."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.delete(
        '/rdrhc-calendar/api/v1/shifts/{}/delete/'.format(token.user.id)
    )

    assert response.status_code == 204

def test__user_schedule_upload__403_response_on_anonymous_user(user):
    """Test for 403 response on anonymous user."""
    # Set up client and response
    client = APIClient()
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_schedule_upload',
        kwargs={'user_id': user.id}
    ))

    assert response.status_code == 403

def test__user_schedule_upload__403_response_on_user_without_permissions(user):
    """Test for 403 response on user without permission."""
    # Create token and add user permissions
    token = utils.create_token(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_schedule_upload', kwargs={'user_id': token.user.id}
    ))

    assert response.status_code == 403

def test__user_schedule_upload__200_response_on_user_with_permissions(calendar_user):
    """Test for 200 response on user with permission."""
    # Create token and add user permissions
    token = utils.create_token(calendar_user.sb_user)
    utils.add_api_permission(calendar_user.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.post(reverse(
        'rdrhc_calendar:api_v1:user_schedule_upload',
        kwargs={'user_id': token.user.id}
    ))

    assert response.status_code == 200

def test__user_schedule_upload__accessible_by_url(calendar_user):
    """Tests that endpoint exists at expected URL."""
    # Create token and add user permissions
    token = utils.create_token(calendar_user.sb_user)
    utils.add_api_permission(calendar_user.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.post(
        '/rdrhc-calendar/api/v1/shifts/{}/upload/'.format(token.user.id)
    )
    print(response.content)
    assert response.status_code == 200

def test__user_email_first_sent__403_response_on_anonymous_user(user):
    """Test for 403 response on anonymous user."""
    # Set up client and response
    client = APIClient()
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_email_first_sent',
        kwargs={'user_id': user.id}
    ))

    assert response.status_code == 403

def test__user_email_first_sent__403_response_on_user_without_permissions(user):
    """Test for 403 response on user without permission."""
    # Create token and add user permissions
    token = utils.create_token(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:user_email_first_sent',
        kwargs={'user_id': token.user.id}
    ))

    assert response.status_code == 403

def test__user_email_first_sent__200_response_on_user_with_permissions(calendar_user):
    """Test for 200 response on user with permission."""
    # Create token and add user permissions
    token = utils.create_token(calendar_user.sb_user)
    utils.add_api_permission(calendar_user.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.post(reverse(
        'rdrhc_calendar:api_v1:user_email_first_sent',
        kwargs={'user_id': token.user.id}
    ))

    assert response.status_code == 200

def test__user_email_first_sent__accessible_by_url(calendar_user):
    """Tests that endpoint exists at expected URL."""
    # Create token and add user permissions
    token = utils.create_token(calendar_user.sb_user)
    utils.add_api_permission(calendar_user.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.post(
        '/rdrhc-calendar/api/v1/users/{}/emails/first-sent/'.format(token.user.id)
    )

    assert response.status_code == 200

def test__missing_shift_code_upload__403_response_on_anonymous_user():
    """Test for 403 response on anonymous user."""
    # Set up client and response
    client = APIClient()
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:missing_shift_codes_upload'
    ))

    assert response.status_code == 403

def test__missing_shift_code_upload__403_response_on_user_without_permissions(user):
    """Test for 403 response on user without permission."""
    # Create token and add user permissions
    token = utils.create_token(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.get(reverse(
        'rdrhc_calendar:api_v1:missing_shift_codes_upload'
    ))

    assert response.status_code == 403

def test__missing_shift_code_upload__200_response_on_user_with_permissions(user):
    """Test for 200 response on user with permission."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.post(reverse(
        'rdrhc_calendar:api_v1:missing_shift_codes_upload'
    ))

    assert response.status_code == 200

def test__missing_shift_code_upload__accessible_by_url(user):
    """Tests that endpoint exists at expected URL."""
    # Create token and add user permissions
    token = utils.create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
    response = client.post(
        '/rdrhc-calendar/api/v1/shift-codes/missing/upload/'
    )

    assert response.status_code == 200
