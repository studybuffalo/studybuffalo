"""Tests for the RDRHC Calendar URLs."""
import pytest

from django.test import Client
from django.urls import reverse

from rdrhc_calendar import models, views
from rdrhc_calendar.tests import utils


pytestmark = pytest.mark.django_db

def test__calendar_index__302_response_if_not_logged_in():
    """Tests for 302 response if user not logged in."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('rdrhc_calendar:index'))

    assert response.status_code == 302

def test__calendar_index__403_response_if_not_authorized(user):
    """Tests for 403 response if user does not have permissions."""
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('rdrhc_calendar:index'))

    assert response.status_code == 403

def test__calendar_index__200_response_if_authorized(user):
    """Tests for 200 response when user is logged in with permissions."""
    # Add permission to user
    utils.add_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('rdrhc_calendar:index'))

    # Check that user logged in
    assert str(response.context['user']) == str(user)

    # Check for 200 response
    assert response.status_code == 200

def test__calendar_index__url_exists_at_desired_location(user):
    # Add permission to user
    utils.add_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('rdrhc_calendar:index'))

    assert response.status_code == 200

def test__calendar_settings__302_response_if_not_logged_in():
    """Tests for 302 response if user is not logged in."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('rdrhc_calendar:settings'))

    assert response.status_code == 302

def test__calendar_settings__403_response_if_not_authorized(user):
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('rdrhc_calendar:settings'))

    assert response.status_code == 403

def test__calendar_settings__404_response_if_authorized_but_no_calendar(user):
    """Test 404 response if user doesn't have a calendar."""
    # Add permission to user
    utils.add_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('rdrhc_calendar:settings'))

    assert response.status_code == 404

def test__calendar_settings__200_response_if_authorized(calendar_user):
    """Test for 200 response if user is authorized with calendar."""
    # Add permission to user
    utils.add_view_permission(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.get(reverse('rdrhc_calendar:settings'))

    # Check that user logged in
    assert response.context['user'] == calendar_user.sb_user
    assert response.status_code == 200

def test__calendar_settings__url_exists_at_desired_location(calendar_user):
    """Test that URL exists at desired location."""
    # Add permission to user
    utils.add_view_permission(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.get(reverse('rdrhc_calendar:settings'))

    assert response.status_code == 200

def test__shift_code_list__302_response_if_not_logged_in():
    """Tests for 302 response if user is not logged in."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('rdrhc_calendar:code_list'))

    assert response.status_code == 302

def test__shift_code_list__403_response_if_not_authorized(user):
    """Tests for 403 response if user does not have permissions."""
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('rdrhc_calendar:code_list'))

    assert response.status_code == 403

def test__shift_code_list__404_response_if_authorized_but_no_calendar(user):
    """Test 404 response if user doesn't have a calendar."""
    # Add permission to user
    utils.add_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('rdrhc_calendar:code_list'))

    assert response.status_code == 404

def test__shift_code_list__200_response_if_authorized(calendar_user):
    """Tests for 200 response when user is logged in with permissions."""
    # Add permission to user
    utils.add_view_permission(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.get(reverse('rdrhc_calendar:code_list'))

    # Check that user logged in
    assert response.context['user'] == calendar_user.sb_user
    assert response.status_code == 200

def test__shift_code_list__settings_url_exists_at_desired_location(calendar_user):
    """Test that URL exists at desired location."""
    # Add permission to user
    utils.add_view_permission(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.get('/rdrhc-calendar/shifts/')

    assert response.status_code == 200

def test__calendar_code_edit__302_response_if_not_logged_in(shift_code):
    """Tests for 302 response if user is not logged in."""
    # Set up client and response
    client = Client()
    response = client.get(reverse(
        'rdrhc_calendar:code_edit',
        kwargs={'code_id': shift_code.id},
    ))
    assert response.status_code == 302

def test__calendar_code_edit__403_response_if_not_authorized(shift_code):
    """Tests for 403 response if user does not have permissions."""
    client = Client()
    client.force_login(user=shift_code.sb_user)
    response = client.get(reverse(
        'rdrhc_calendar:code_edit',
        kwargs={'code_id': shift_code.id},
    ))

    assert response.status_code == 403

def test__calendar_code_edit__404_response_if_authorized_but_no_calendar(user, shift_code):
    """Test 404 response if user doesn't have a calendar."""
    # Add permission to user
    utils.add_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse(
        'rdrhc_calendar:code_edit',
        kwargs={'code_id': shift_code.id},
    ))

    assert response.status_code == 404

def test__calendar_code_edit__200_response_if_authorized(shift_code):
    """Tests for 200 response when user is logged in with permissions."""
    # Add permission to user
    utils.add_view_permission(shift_code.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=shift_code.sb_user)
    response = client.get(reverse(
        'rdrhc_calendar:code_edit',
        kwargs={'code_id': shift_code.id},
    ))

    # Check that user logged in
    assert response.context['user'] == shift_code.sb_user
    assert response.status_code == 200

def test__calendar_code_edit__url_exists_at_desired_location(shift_code):
    """Test that URL exists at desired location."""
    # Add permission to user
    utils.add_view_permission(shift_code.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=shift_code.sb_user)
    response = client.get('/rdrhc-calendar/shifts/{}/'.format(shift_code.id))

    assert response.status_code == 200

def test__calendar_code_add__302_response_if_not_logged_in():
    """Tests for 302 response if user is not logged in."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('rdrhc_calendar:code_add'))

    assert response.status_code == 302

def test__calendar_code_add__403_response_if_not_authorized(user):
    """Tests for 403 response if user does not have permissions."""
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('rdrhc_calendar:code_add'))

    assert response.status_code == 403

def test__calendar_code_add__404_response_if_authorized_but_no_calendar(user):
    """Test 404 response if user doesn't have a calendar."""
    # Add permission to user
    utils.add_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('rdrhc_calendar:code_add'))

    assert response.status_code == 404

def test__calendar_code_add__200_response_if_authorized(calendar_user):
    """Tests for 200 response when user is logged in with permissions."""
    # Add permission to user
    utils.add_view_permission(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.get(reverse('rdrhc_calendar:code_add'))

    # Check that user logged in
    assert response.context['user'] == calendar_user.sb_user
    assert response.status_code == 200

def test__calendar_code_add__url_exists_at_desired_location(calendar_user):
    """Test that URL exists at desired location."""
    # Add permission to user
    utils.add_view_permission(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.get('/rdrhc-calendar/shifts/add/')

    assert response.status_code == 200

def test__calendar_code_delete__302_response_if_not_logged_in(shift_code):
    """Tests for 302 response if user is not logged in."""
    # Set up client and response
    client = Client()
    response = client.get(reverse(
        'rdrhc_calendar:code_delete',
        kwargs={'code_id': shift_code.id}
    ))

    assert response.status_code == 302

def test__calendar_code_delete__403_response_if_not_authorized(shift_code):
    """Tests for 403 response if user does not have permissions."""
    client = Client()
    client.force_login(user=shift_code.sb_user)
    response = client.get(reverse(
        'rdrhc_calendar:code_delete',
        kwargs={'code_id': shift_code.id}
    ))

    assert response.status_code == 403

def test__calendar_code_delete__404_response_if_authorized_but_no_calendar(shift_code):
    """Test 404 response if user doesn't have a calendar."""
    # Add permission to user
    utils.add_view_permission(shift_code.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=shift_code.sb_user)
    response = client.get(reverse(
        'rdrhc_calendar:code_delete',
        kwargs={'code_id': shift_code.id},
    ))

def test__calendar_code_delete__200_response_if_authorized(shift_code):
    """Tests for 200 response when user is logged in with permissions."""
    # Add permission to user
    utils.add_view_permission(shift_code.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=shift_code.sb_user)
    response = client.get(reverse(
        'rdrhc_calendar:code_delete',
        kwargs={'code_id': shift_code.id},
    ))

    # Check that user logged in
    assert response.context['user'] == shift_code.sb_user
    assert response.status_code == 200

def test__calendar_code_delete__url_exists_at_desired_location(shift_code):
    """Test that URL exists at desired location."""
    # Add permission to user
    utils.add_view_permission(shift_code.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=shift_code.sb_user)
    response = client.get(
        '/rdrhc-calendar/shifts/delete/{}/'.format(shift_code.id)
    )

    assert response.status_code == 200

def test__missing_code_list__302_response_if_not_logged_in():
    """Tests for 302 response if user is not logged in."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('rdrhc_calendar:missing_code_list'))

    assert response.status_code == 302

def test__missing_code_list__403_response_if_not_authorized(user):
    """Tests for 403 response if user does not have permissions."""
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('rdrhc_calendar:missing_code_list'))

    assert response.status_code == 403

def test__missing_code_list__200_response_if_authorized(calendar_user):
    """Tests for 200 response when user is logged in with permissions."""
    # Add permission to user
    utils.add_add_default_codes_permissions(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.get(reverse('rdrhc_calendar:missing_code_list'))

    # Check that user logged in
    assert response.context['user'] == calendar_user.sb_user
    assert response.status_code == 200

def test__missing_code_list__url_exists_at_desired_location(calendar_user):
    """Test that URL exists at desired location."""
    # Add permission to user
    utils.add_add_default_codes_permissions(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.get('/rdrhc-calendar/missing-codes/')

    assert response.status_code == 200

def test__missing_code_edit__302_response_if_not_logged_in(missing_shift_code):
    """Tests for 302 response if user is not logged in."""
    # Set up client and response
    client = Client()
    response = client.get(reverse(
        'rdrhc_calendar:missing_code_edit',
        kwargs={'code_id': missing_shift_code.id},
    ))
    assert response.status_code == 302

def test__missing_code_edit__403_response_if_not_authorized(user, missing_shift_code):
    """Tests for 403 response if user does not have permissions."""
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse(
        'rdrhc_calendar:missing_code_edit',
        kwargs={'code_id': missing_shift_code.id},
    ))

    assert response.status_code == 403

def test__missing_code_edit__200_response_if_authorized(calendar_user, missing_shift_code):
    """Tests for 200 response when user is logged in with permissions."""
    # Add permission to user
    utils.add_add_default_codes_permissions(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.get(reverse(
        'rdrhc_calendar:missing_code_edit',
        kwargs={'code_id': missing_shift_code.id},
    ))

    # Check that user logged in
    assert response.context['user'] == calendar_user.sb_user
    assert response.status_code == 200

def test__missing_code_edit__url_exists_at_desired_location(calendar_user, missing_shift_code):
    """Test that URL exists at desired location."""
    # Add permission to user
    utils.add_add_default_codes_permissions(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.get(
        '/rdrhc-calendar/missing-codes/edit/{}/'.format(missing_shift_code.id)
    )

    assert response.status_code == 200

def test__missing_code_delete__302_response_if_not_logged_in(missing_shift_code):
    """Tests for 302 response if user is not logged in."""
    # Set up client and response
    client = Client()
    response = client.get(reverse(
        'rdrhc_calendar:missing_code_delete',
        kwargs={'code_id': missing_shift_code.id},
    ))

    assert response.status_code == 302

def test__missing_code_delete__403_response_if_not_authorized(user, missing_shift_code):
    """Tests for 403 response if user does not have permissions."""
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse(
        'rdrhc_calendar:missing_code_delete',
        kwargs={'code_id': missing_shift_code.id},
    ))

    assert response.status_code == 403

def test__missing_code_delete__200_response_if_authorized(calendar_user, missing_shift_code):
    """Tests for 200 response when user is logged in with permissions."""
    # Add permission to user
    utils.add_add_default_codes_permissions(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.get(reverse(
        'rdrhc_calendar:missing_code_delete',
        kwargs={'code_id': missing_shift_code.id},
    ))

    # Check that user logged in
    assert response.context['user'] == calendar_user.sb_user
    assert response.status_code == 200

def test__missing_code_delete__url_exists_at_desired_location(calendar_user, missing_shift_code):
    """Test that URL exists at desired location."""
    # Add permission to user
    utils.add_add_default_codes_permissions(calendar_user.sb_user)

    # Set up client and response
    client = Client()
    client.force_login(user=calendar_user.sb_user)
    response = client.get(
        '/rdrhc-calendar/missing-codes/delete/{}/'.format(missing_shift_code.id)
    )

    assert response.status_code == 200
