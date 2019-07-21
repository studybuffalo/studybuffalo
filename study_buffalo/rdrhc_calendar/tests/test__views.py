"""Tests for the RDRHC Calendar views."""
from unittest.mock import patch

import pytest

from django.db import IntegrityError
from django.test import Client
from django.urls import reverse

from rdrhc_calendar import models, views
from rdrhc_calendar.tests import utils


pytestmark = pytest.mark.django_db

def mock_missing_code_form_save(self, commit=False):
    raise IntegrityError

def test__calendar_index__template(user):
    """Test for proper template in calendar_index view."""
    # Add permission to user
    utils.add_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('rdrhc_calendar:index'))

    # Test for template
    assert (
        'rdrhc_calendar/index.html' in [t.name for t in response.templates]
    )

def test__calendar_settings__template(calendar_user):
    """Test for proper template in calendar_setttings views."""
    # Add permission to user
    utils.add_view_permission(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.get(reverse('rdrhc_calendar:settings'))

    # Test for template
    assert (
        'rdrhc_calendar/calendar_settings.html' in [t.name for t in response.templates]
    )

def test__calendar_settings__redirect_on_valid_post(calendar_user):
    """Test for proper redirection on valid post."""
    # Add permission to user
    utils.add_view_permission(calendar_user.sb_user)

    # Create valid data
    valid_data = {
        'calendar_name': 'SecretCalendar',
        'full_day': False,
        'reminder': '',
    }

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.post(reverse('rdrhc_calendar:settings'), valid_data)

    # Confirm response status_code
    assert response.status_code == 302

def test__shift_code_list__template(calendar_user):
    """Test for proper template in shift_code_list views."""
    # Add permission to user
    utils.add_view_permission(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.get(reverse('rdrhc_calendar:code_list'))

    # Test for template
    assert (
        'rdrhc_calendar/shiftcode_list.html' in [t.name for t in response.templates]
    )

def test__shift_code_edit__template(shift_code):
    """Test for proper template in shift_code_edit views."""
    # Add permission to user
    utils.add_view_permission(shift_code.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=shift_code.sb_user)
    response = client.get(reverse(
        'rdrhc_calendar:code_edit',
        kwargs={'code_id': shift_code.id},
    ))

    # Test for template
    assert (
        'rdrhc_calendar/shiftcode_edit.html' in [t.name for t in response.templates]
    )

def test__shift_code_edit__redirect_on_valid_post(shift_code):
    """Test for proper redirection on valid posts."""
    valid_data = {
        'code': 'A2',
        'monday_start': '01:00:00',
        'monday_duration': '1.1',
        'tuesday_start': '02:00:00',
        'tuesday_duration': '2.2',
        'wednesday_start': '03:00:00',
        'wednesday_duration': '3.3',
        'thursday_start': '04:00:00',
        'thursday_duration': '4.4',
        'friday_start': '05:00:00',
        'friday_duration': '5.5',
        'saturday_start': '06:00:00',
        'saturday_duration': '6.6',
        'sunday_start': '07:00:00',
        'sunday_duration': '7.7',
        'stat_start': '08:00:00',
        'stat_duration': '8.8',
    }

    # Add permission to user
    utils.add_view_permission(shift_code.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=shift_code.sb_user)
    response = client.post(
        reverse('rdrhc_calendar:code_edit', kwargs={'code_id': shift_code.id}),
        valid_data,
    )

    assert response.status_code == 302

def test__shift_code_add__template(calendar_user):
    """Test for proper template in shift_code_add views."""
    # Add permission to user
    utils.add_view_permission(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.get(reverse('rdrhc_calendar:code_add'))

    # Test for template
    assert (
        'rdrhc_calendar/shiftcode_add.html' in [t.name for t in response.templates]
    )

def test__shift_code_add__redirect_on_valid_post(calendar_user):
    """Test for proper redirection on valid post."""
    valid_data = {
        'code': 'A1',
        'monday_start': '01:00:00',
        'monday_duration': '1.1',
        'tuesday_start': '02:00:00',
        'tuesday_duration': '2.2',
        'wednesday_start': '03:00:00',
        'wednesday_duration': '3.3',
        'thursday_start': '04:00:00',
        'thursday_duration': '4.4',
        'friday_start': '05:00:00',
        'friday_duration': '5.5',
        'saturday_start': '06:00:00',
        'saturday_duration': '6.6',
        'sunday_start': '07:00:00',
        'sunday_duration': '7.7',
        'stat_start': '08:00:00',
        'stat_duration': '8.8',
    }

    # Add permission to user
    utils.add_view_permission(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.post(reverse('rdrhc_calendar:code_add'), valid_data)

    assert response.status_code == 302

def test_entry_is_added_on_valid_post(calendar_user):
    """Tests model entry is properly added on valid post."""
    valid_data = {
        'code': 'A1',
        'monday_start': '01:00:00',
        'monday_duration': '1.1',
        'tuesday_start': '02:00:00',
        'tuesday_duration': '2.2',
        'wednesday_start': '03:00:00',
        'wednesday_duration': '3.3',
        'thursday_start': '04:00:00',
        'thursday_duration': '4.4',
        'friday_start': '05:00:00',
        'friday_duration': '5.5',
        'saturday_start': '06:00:00',
        'saturday_duration': '6.6',
        'sunday_start': '07:00:00',
        'sunday_duration': '7.7',
        'stat_start': '08:00:00',
        'stat_duration': '8.8',
    }

    # Get current count of model
    shift_code_count = models.ShiftCode.objects.count()

    # Add permission to user
    utils.add_view_permission(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.post(reverse('rdrhc_calendar:code_add'), valid_data)

    assert models.ShiftCode.objects.count() == shift_code_count + 1

def test__shift_code_delete__template(shift_code):
    """Test for proper template in shift_code_delete views."""
    # Add permission to user
    utils.add_view_permission(shift_code.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=shift_code.sb_user)
    response = client.get(reverse(
        'rdrhc_calendar:code_delete',
        kwargs={'code_id': shift_code.id},
    ))

    # Test for template
    assert (
        'rdrhc_calendar/shiftcode_delete.html' in [t.name for t in response.templates]
    )

def test__shift_code_delete__redirect_on_valid_post(shift_code):
    """Test for proper redirection on valid post."""
    # Add permission to user
    utils.add_view_permission(shift_code.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=shift_code.sb_user)
    response = client.post(reverse(
        'rdrhc_calendar:code_delete', kwargs={'code_id': shift_code.id}
    ))

    assert response.status_code == 302

def test__shift_code_delete__instance_deleted_on_valid_post(shift_code):
    """Tests model entry is properly deleted on valid post."""
    # Get current model count
    shift_code_count = models.ShiftCode.objects.count()

    # Add permission to user
    utils.add_view_permission(shift_code.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=shift_code.sb_user)
    response = client.post(reverse(
        'rdrhc_calendar:code_delete', kwargs={'code_id': shift_code.id}
    ))

    assert models.ShiftCode.objects.count() == shift_code_count - 1

def test__missing_code_list__template(user):
    """Test for proper template in missing_code_list views."""
    # Add permission to user
    utils.add_add_default_codes_permissions(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('rdrhc_calendar:missing_code_list'))

    # Test for template
    assert (
        'rdrhc_calendar/missingshiftcode_list.html' in [t.name for t in response.templates]
    )

def test__missing_code_edit__template(user, missing_shift_code):
    """Test for proper template in missing_code_edit views."""
    # Add permission to user
    utils.add_add_default_codes_permissions(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse(
        'rdrhc_calendar:missing_code_edit',
        kwargs={'code_id': missing_shift_code.id},
    ))

    # Test for template
    assert (
        'rdrhc_calendar/missingshiftcode_edit.html' in [t.name for t in response.templates]
    )

def test__missing_code_edit__redirect_on_valid_post(user, missing_shift_code):
    """Test for proper redirection on valid post."""
    valid_data = {
        'monday_start': '01:00:00',
        'monday_duration': '1.1',
        'tuesday_start': '02:00:00',
        'tuesday_duration': '2.2',
        'wednesday_start': '03:00:00',
        'wednesday_duration': '3.3',
        'thursday_start': '04:00:00',
        'thursday_duration': '4.4',
        'friday_start': '05:00:00',
        'friday_duration': '5.5',
        'saturday_start': '06:00:00',
        'saturday_duration': '6.6',
        'sunday_start': '07:00:00',
        'sunday_duration': '7.7',
        'stat_start': '08:00:00',
        'stat_duration': '8.8',
    }

    # Add permission to user
    utils.add_add_default_codes_permissions(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.post(
        reverse(
            'rdrhc_calendar:missing_code_edit',
            kwargs={'code_id': missing_shift_code.id}
        ),
        valid_data,
    )

    assert response.status_code == 302

@patch('rdrhc_calendar.views.MissingCodeForm.save', mock_missing_code_form_save)
def test__mising_code_edit__unique_validation(user, missing_shift_code):
    """Tests that unique code is properly maintained."""
    valid_data = {
        'monday_start': '01:00:00',
        'monday_duration': '1.1',
        'tuesday_start': '02:00:00',
        'tuesday_duration': '2.2',
        'wednesday_start': '03:00:00',
        'wednesday_duration': '3.3',
        'thursday_start': '04:00:00',
        'thursday_duration': '4.4',
        'friday_start': '05:00:00',
        'friday_duration': '5.5',
        'saturday_start': '06:00:00',
        'saturday_duration': '6.6',
        'sunday_start': '07:00:00',
        'sunday_duration': '7.7',
        'stat_start': '08:00:00',
        'stat_duration': '8.8',
    }

    # Add permission to user
    utils.add_add_default_codes_permissions(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)

    # Trigger IntegrityError
    try:
        response = client.post(
            reverse(
                'rdrhc_calendar:missing_code_edit',
                kwargs={'code_id': missing_shift_code.id}
            ),
            valid_data,
        )
    except IntegrityError:
        assert True
    else:
        assert False

def test__missing_code_delete__template(user, missing_shift_code):
    """Test for proper template in missing_code_delete views."""
    # Add permission to user
    utils.add_add_default_codes_permissions(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse(
        'rdrhc_calendar:missing_code_delete',
        kwargs={'code_id': missing_shift_code.id},
    ))

    # Test for template
    assert (
        'rdrhc_calendar/missingshiftcode_delete.html' in [t.name for t in response.templates]
    )

def test__missing_code_delete__redirect_on_valid_post(user, missing_shift_code):
    """Test for proper redirection on valid post."""
    # Add permission to user
    utils.add_add_default_codes_permissions(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.post(reverse(
        'rdrhc_calendar:missing_code_delete', kwargs={'code_id': missing_shift_code.id}
    ))

    assert response.status_code == 302

def test__missing_code_delete__instance_deleted_on_valid_post(user, missing_shift_code):
    """Tests model entry is properly deleted on valid post."""
    # Get current model count
    missing_count = models.MissingShiftCode.objects.count()

    # Add permission to user
    utils.add_add_default_codes_permissions(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.post(reverse(
        'rdrhc_calendar:missing_code_delete', kwargs={'code_id': missing_shift_code.id}
    ))

    assert models.MissingShiftCode.objects.count() == missing_count - 1
