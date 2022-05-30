"""Tests for the HC DPD API views."""
import json

import pytest

from django.urls import reverse

from allauth.account.models import EmailAddress
from rest_framework.test import APIClient

from rdrhc_calendar.models import CalendarUser, Shift, MissingShiftCode
from rdrhc_calendar.tests import utils
from users.tests.utils import create_token


pytestmark = pytest.mark.django_db


# TODO: test handling of checksum list with no params & invalid methods

def test__user_list__returns_user_list(calendar_user):
    """Tests that proper response is returned."""
    # Create token and add user permissions
    token = create_token(calendar_user.sb_user)
    utils.add_api_permission(calendar_user.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(reverse('api:rdrhc_calendar_v1:user_list'))
    content = json.loads(response.content)  # pylint: disable=no-member

    # Confirm types returned
    assert isinstance(content, list)
    assert isinstance(content[0]['id'], int)
    assert isinstance(content[0]['sb_user'], int)
    assert isinstance(content[0]['name'], str)
    assert isinstance(content[0]['schedule_name'], str)
    assert isinstance(content[0]['calendar_name'], str)
    assert isinstance(content[0]['role'], str)
    assert isinstance(content[0]['first_email_sent'], bool)
    assert isinstance(content[0]['full_day'], bool)
    assert isinstance(content[0]['reminder'], int)

    # Confirm right model instance is pulled
    assert content[0]['id'] == calendar_user.id


def test__user_detail__returns_user_detail(calendar_user):
    """Tests that proper response is returned."""
    # Create token and add user permissions
    token = create_token(calendar_user.sb_user)
    utils.add_api_permission(calendar_user.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(reverse(
        'api:rdrhc_calendar_v1:user_detail',
        kwargs={'user_id': calendar_user.id}
    ))
    content = json.loads(response.content)

    # Confirm types returned
    assert isinstance(content['id'], int)
    assert isinstance(content['sb_user'], int)
    assert isinstance(content['name'], str)
    assert isinstance(content['schedule_name'], str)
    assert isinstance(content['calendar_name'], str)
    assert isinstance(content['role'], str)
    assert isinstance(content['first_email_sent'], bool)
    assert isinstance(content['full_day'], bool)
    assert isinstance(content['reminder'], int)

    # Confirm right model instance is pulled
    assert content['id'] == calendar_user.id


def test__user_email_list__returns_user_email_list(user):
    """Tests that proper response is returned."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_permission(user)

    # Add email for user
    EmailAddress.objects.create(user=user, email='email@email.com')

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(reverse(
        'api:rdrhc_calendar_v1:user_email_list',
        kwargs={'user_id': token.user.id}
    ))
    content = json.loads(response.content)  # pylint: disable=no-member

    # Confirm types and value returned
    assert isinstance(content, list)
    assert content[0] == 'email@email.com'


def test__shift_list__returns_shift_list(shift):
    """Tests that proper response is returned."""
    # Create token and add user permissions
    token = create_token(shift.sb_user)
    utils.add_api_permission(shift.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(reverse('api:rdrhc_calendar_v1:shift_list'))
    content = json.loads(response.content)

    # Confirm types and value returned
    assert isinstance(content, list)
    assert isinstance(content[0]['id'], int)
    assert isinstance(content[0]['sb_user'], int)
    assert isinstance(content[0]['date'], str)
    assert isinstance(content[0]['shift_code'], int)
    assert isinstance(content[0]['text_shift_code'], str)
    assert content[0]['id'] == shift.id


def test_api_returns_user_shift_code_list(shift_code):
    """Tests that proper response is returned."""
    # Create token and add user permissions
    token = create_token(shift_code.sb_user)
    utils.add_api_permission(shift_code.sb_user)

    # Add a calendar to the user
    CalendarUser.objects.create(
        sb_user=shift_code.sb_user,
    )

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(reverse(
        'api:rdrhc_calendar_v1:user_shift_codes_list',
        kwargs={'user_id': token.user.id}
    ))
    content = json.loads(response.content)

    # Confirm types and value returned
    assert isinstance(content, list)
    assert isinstance(content[0]['id'], int)
    assert isinstance(content[0]['code'], str)
    assert isinstance(content[0]['monday_start'], str)
    assert isinstance(content[0]['monday_duration'], str)
    assert isinstance(content[0]['tuesday_start'], str)
    assert isinstance(content[0]['tuesday_duration'], str)
    assert isinstance(content[0]['wednesday_start'], str)
    assert isinstance(content[0]['wednesday_duration'], str)
    assert isinstance(content[0]['thursday_start'], str)
    assert isinstance(content[0]['thursday_duration'], str)
    assert isinstance(content[0]['friday_start'], str)
    assert isinstance(content[0]['friday_duration'], str)
    assert isinstance(content[0]['saturday_start'], str)
    assert isinstance(content[0]['saturday_duration'], str)
    assert isinstance(content[0]['sunday_start'], str)
    assert isinstance(content[0]['sunday_duration'], str)
    assert isinstance(content[0]['stat_start'], str)
    assert isinstance(content[0]['stat_duration'], str)
    assert content[0]['id'] == shift_code.id


def test_api_returns_user_shift_code_list__default_codes(shift_code):
    """Tests that default codes are returned when applicable."""
    sb_user = shift_code.sb_user

    # Create token and add user permissions
    token = create_token(sb_user)
    utils.add_api_permission(sb_user)

    # Add a calendar to the user
    CalendarUser.objects.create(
        sb_user=sb_user,
        role='p',
    )

    # Setup shift code to function as a default code (no user, same role)
    shift_code.sb_user = None
    shift_code.role = 'p'
    shift_code.save()

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(reverse(
        'api:rdrhc_calendar_v1:user_shift_codes_list',
        kwargs={'user_id': token.user.id}
    ))
    content = json.loads(response.content)

    # Confirm types and value returned
    assert isinstance(content, list)
    assert isinstance(content[0]['id'], int)
    assert isinstance(content[0]['code'], str)
    assert isinstance(content[0]['monday_start'], str)
    assert isinstance(content[0]['monday_duration'], str)
    assert isinstance(content[0]['tuesday_start'], str)
    assert isinstance(content[0]['tuesday_duration'], str)
    assert isinstance(content[0]['wednesday_start'], str)
    assert isinstance(content[0]['wednesday_duration'], str)
    assert isinstance(content[0]['thursday_start'], str)
    assert isinstance(content[0]['thursday_duration'], str)
    assert isinstance(content[0]['friday_start'], str)
    assert isinstance(content[0]['friday_duration'], str)
    assert isinstance(content[0]['saturday_start'], str)
    assert isinstance(content[0]['saturday_duration'], str)
    assert isinstance(content[0]['sunday_start'], str)
    assert isinstance(content[0]['sunday_duration'], str)
    assert isinstance(content[0]['stat_start'], str)
    assert isinstance(content[0]['stat_duration'], str)
    assert content[0]['id'] == shift_code.id


def test__stat_holiday_list__returns_list_without_parameters(user):
    """Tests that proper response is returned."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_permission(user)

    # Create stat holidsy
    utils.create_stat_holidays()

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(reverse('api:rdrhc_calendar_v1:stat_holidays_list'))
    content = json.loads(response.content)

    # Confirm types and value returned
    assert isinstance(content, list)
    assert len(content) == 10
    assert isinstance(content[0], str)


def test__stat_holiday_list__returns_list_with_parameters(user):
    """Tests that proper response is returned when parameters added."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_permission(user)

    # Create stat holidsy
    utils.create_stat_holidays()

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(
        reverse('api:rdrhc_calendar_v1:stat_holidays_list'),
        {'date_start': '2014-01-01', 'date_end': '2018-12-31'}
    )
    content = json.loads(response.content)

    # Confirm proper amount of dates returned
    assert len(content) == 5


def test__user_schedule_list__returns_list(shift):
    """Tests that proper response is returned."""
    # Create token and add user permissions
    token = create_token(shift.sb_user)
    utils.add_api_permission(shift.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(reverse(
        'api:rdrhc_calendar_v1:user_schedule_list',
        kwargs={'user_id': token.user.id}
    ))
    content = json.loads(response.content)

    # Confirm proper response and types are returned
    assert isinstance(content, list)
    assert isinstance(content[0]['shift_code'], int)
    assert isinstance(content[0]['date'], str)
    assert isinstance(content[0]['text_shift_code'], str)
    assert content[0]['id'] == shift.id


def test__user_schedule_delete__deletes_schedule(shift):
    """Tests that proper response is returned."""
    # Confirm shift exists
    assert Shift.objects.filter(sb_user=shift.sb_user).count() == 1

    # Create token and add user permissions
    token = create_token(shift.sb_user)
    utils.add_api_permission(shift.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    client.delete(reverse(
        'api:rdrhc_calendar_v1:user_schedule_delete',
        kwargs={'user_id': token.user.id}
    ))

    assert Shift.objects.filter(sb_user=shift.sb_user).count() == 0


def test__user_schedule_upload__uploads_user_schedule(calendar_user):
    """Tests that proper response is returned."""
    # Create token and add user permissions
    user = calendar_user.sb_user
    token = create_token(user)
    utils.add_api_permission(user)

    # Confirm no shifts exist
    assert Shift.objects.filter(sb_user=user).count() == 0

    # Setup POST data
    data = {
        'schedule': [
            {
                'sb_user': user.id,
                'date': '2018-02-01',
                'shift_code': '',
                'text_shift_code': 'A3'
            },
            {
                'sb_user': user.id,
                'date': '2018-02-02',
                'shift_code': '',
                'text_shift_code': 'A4'
            },
            {
                'sb_user': user.id,
                'date': '2018-02-03',
                'shift_code': '',
                'text_shift_code': 'A5'
            }
        ]
    }

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    client.post(
        reverse(
            'api:rdrhc_calendar_v1:user_schedule_upload',
            kwargs={'user_id': token.user.id}
        ),
        json.dumps(data),
        content_type='application/json',
    )

    # Confirm shift exists
    assert Shift.objects.filter(sb_user=user).count() == 3


def test__user_schedule_upload__json_error(calendar_user):
    """Tests that handling of JSON error."""
    # Create token and add user permissions
    user = calendar_user.sb_user
    token = create_token(user)
    utils.add_api_permission(user)

    # Confirm no shifts exist
    assert Shift.objects.filter(sb_user=user).count() == 0

    # Setup POST data
    data = {
        'schedule': [
            {
                'sb_user': user.id,
                'date': '2018-02-01',
                'shift_code': '',
                'text_shift_code': 'A3'
            },
            {
                'sb_user': user.id,
                'date': '2018-02-02',
                'shift_code': '',
                'text_shift_code': 'A4'
            },
            {
                'sb_user': user.id,
                'date': '2018-02-03',
                'shift_code': '',
                'text_shift_code': 'A5'
            }
        ]
    }
    json_str = json.dumps(data)
    json_error = f'<{json_str}>'

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse(
            'api:rdrhc_calendar_v1:user_schedule_upload',
            kwargs={'user_id': token.user.id}
        ),
        json_error,
        content_type='application/json',
    )

    #  Confirm error status code
    assert response.status_code == 400

    # Confirm error response
    assert 'JSON parse error' in str(response.content)


def test__user_schedule_upload__400_response_on_invalid_data(calendar_user):
    """Confirms error handling with invalid data."""
    # Create token and add user permissions
    user = calendar_user.sb_user
    token = create_token(user)
    utils.add_api_permission(user)

    # Setup POST data
    data = {
        'schedule': [
            {
                'sb_user': user.id,
                'date': '2018-02-01',
                'shift_code': 'abc',
                'text_shift_code': 'A3'
            },
        ]
    }

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse(
            'api:rdrhc_calendar_v1:user_schedule_upload',
            kwargs={'user_id': token.user.id}
        ),
        json.dumps(data),
        content_type='application/json',
    )
    content = json.loads(response.content)

    assert response.status_code == 400
    assert 'errors' in content


def test__user_schedule_upload__400_response_on_invalid_data_format(calendar_user):
    """Confirms error handling when data in incorrect format."""
    # Create token and add user permissions
    user = calendar_user.sb_user
    token = create_token(user)
    utils.add_api_permission(user)

    # Setup POST data
    data = {'schedule': 'abc'}

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse(
            'api:rdrhc_calendar_v1:user_schedule_upload',
            kwargs={'user_id': token.user.id}
        ),
        json.dumps(data),
        content_type='application/json',
    )
    content = json.loads(response.content)

    assert response.status_code == 400
    assert 'errors' in content


def test__user_email_first_sent__confirm_change(calendar_user):
    """Tests that proper response is returned."""
    # Confirm value start off false
    assert calendar_user.first_email_sent is False

    # Create token and add user permissions
    token = create_token(calendar_user.sb_user)
    utils.add_api_permission(calendar_user.sb_user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    client.post(reverse(
        'api:rdrhc_calendar_v1:user_email_first_sent',
        kwargs={'user_id': token.user.id}
    ))

    # Retrieve updated database entry and confirm its value
    calendar_user.refresh_from_db()
    assert calendar_user.first_email_sent is True


def test__missing_shift_code_upload__uploads_missing_codes(user):
    """Tests that proper response is returned."""
    # Confirm no values
    assert MissingShiftCode.objects.all().count() == 0

    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse('api:rdrhc_calendar_v1:missing_shift_codes_upload'),
        json.dumps({'codes': [{'code': 'A1', 'role': 'p'}]}),
        content_type='application/json',
    )
    print(response.content)
    # Confirm code added
    assert MissingShiftCode.objects.all().count() == 1


def test__missing_shift_code_upload__400_response_on_invalid_data(user):
    """Tests that missing shift code results in 400 response with invalid data."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_permission(user)

    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse('api:rdrhc_calendar_v1:missing_shift_codes_upload'),
        json.dumps({'codes': [{'shift_code': 'abc'}]}),
        content_type='application/json',
    )
    json.loads(response.content)

    assert response.status_code == 400


def test__missing_shift_code_upload__400_response_on_invalid_data_format(user):
    """Tests that missing shift code results in 400 response with invalid format."""
    # Create token and add user permissions
    token = create_token(user)
    utils.add_api_permission(user)

    # Setup JSON format error
    json_str = json.dumps({'codes': [{'code': 'A1', 'role': 'p'}]})
    json_error = f'<{json_str}>'
    # Set up client and response
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.post(
        reverse('api:rdrhc_calendar_v1:missing_shift_codes_upload'),
        json_error,
        content_type='application/json',
    )
    json.loads(response.content)

    assert response.status_code == 400
