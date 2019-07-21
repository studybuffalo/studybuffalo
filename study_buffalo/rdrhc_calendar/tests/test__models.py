"""Tests for the RDRHC Calendar models."""
import pytest

from django.db import IntegrityError

from rdrhc_calendar import models


pytestmark = pytest.mark.django_db

def test__calendar_user__labels(calendar_user):
    """Tests labels of Calendaruser."""
    assert calendar_user._meta.get_field('id').verbose_name == 'ID'
    assert calendar_user._meta.get_field('sb_user').verbose_name == 'SB user'
    assert calendar_user._meta.get_field('name').verbose_name == 'name'
    assert calendar_user._meta.get_field('schedule_name').verbose_name == 'schedule name'
    assert calendar_user._meta.get_field('calendar_name').verbose_name == 'calendar name'
    assert calendar_user._meta.get_field('role').verbose_name == 'role'
    assert calendar_user._meta.get_field('first_email_sent').verbose_name == 'first email sent'
    assert calendar_user._meta.get_field('full_day').verbose_name == 'full day'
    assert calendar_user._meta.get_field('reminder').verbose_name == 'reminder'

def test__calendar_user__max_lengths(calendar_user):
    """Tests max lengths of CalendarUser."""
    assert calendar_user._meta.get_field('name').max_length == 25
    assert calendar_user._meta.get_field('schedule_name').max_length == 25
    assert calendar_user._meta.get_field('calendar_name').max_length == 50
    assert calendar_user._meta.get_field('role').max_length == 1

def test__calendar_user__role_choices(calendar_user):
    """Confirms the choices for CalendarUser roles."""
    choices = calendar_user._meta.get_field('role').choices

    assert ('a', 'Pharmacy Assistant') in choices
    assert ('p', 'Pharmacist') in choices
    assert ('t', 'Pharmacy Technician') in choices

def test__calendar_user__str(calendar_user):
    """Tests CalendarUser __str__ method."""
    assert str(calendar_user) == '{} - {}'.format(calendar_user.role, calendar_user.name)

def test__stat_holiday__labels():
    """Tests the labels of StatHoliday."""
    assert models.StatHoliday._meta.get_field('date').verbose_name == 'date'

def test__stat_holidays__str():
    """Tests the StatHoliday __str__ method."""
    # Create a stat holiday
    stat_holiday = models.StatHoliday.objects.create(
        date='2018-01-01',
    )

    assert str(stat_holiday) == '2018-01-01'

def test__shift_code__labels(shift_code):
    """Tests the ShiftCode labels."""
    assert shift_code._meta.get_field('code').verbose_name == 'code'
    assert shift_code._meta.get_field('sb_user').verbose_name == 'SB user'
    assert shift_code._meta.get_field('role').verbose_name == 'role'
    assert shift_code._meta.get_field('monday_start').verbose_name == 'monday start'
    assert shift_code._meta.get_field('monday_duration').verbose_name == 'monday duration'
    assert shift_code._meta.get_field('tuesday_start').verbose_name == 'tuesday start'
    assert shift_code._meta.get_field('tuesday_duration').verbose_name == 'tuesday duration'
    assert shift_code._meta.get_field('wednesday_start').verbose_name == 'wednesday start'
    assert shift_code._meta.get_field('wednesday_duration').verbose_name == 'wednesday duration'
    assert shift_code._meta.get_field('thursday_start').verbose_name == 'thursday start'
    assert shift_code._meta.get_field('thursday_duration').verbose_name == 'thursday duration'
    assert shift_code._meta.get_field('friday_start').verbose_name == 'friday start'
    assert shift_code._meta.get_field('friday_duration').verbose_name == 'friday duration'
    assert shift_code._meta.get_field('saturday_start').verbose_name == 'saturday start'
    assert shift_code._meta.get_field('saturday_duration').verbose_name == 'saturday duration'
    assert shift_code._meta.get_field('sunday_start').verbose_name == 'sunday start'
    assert shift_code._meta.get_field('sunday_duration').verbose_name == 'sunday duration'
    assert shift_code._meta.get_field('stat_start').verbose_name == 'stat start'
    assert shift_code._meta.get_field('stat_duration').verbose_name == 'stat duration'

def test__shift_code__max_lengths(shift_code):
    """Tests the ShiftCode max_lengths."""
    assert shift_code._meta.get_field('code').max_length == 20
    assert shift_code._meta.get_field('role').max_length == 1

def test__shift_code__decimal_maxes(shift_code):
    """Tests the ShiftCode max_decimal."""
    assert shift_code._meta.get_field('monday_duration').decimal_places == 2
    assert shift_code._meta.get_field('monday_duration').max_digits == 4
    assert shift_code._meta.get_field('tuesday_duration').decimal_places == 2
    assert shift_code._meta.get_field('tuesday_duration').max_digits == 4
    assert shift_code._meta.get_field('wednesday_duration').decimal_places == 2
    assert shift_code._meta.get_field('wednesday_duration').max_digits == 4
    assert shift_code._meta.get_field('thursday_duration').decimal_places == 2
    assert shift_code._meta.get_field('thursday_duration').max_digits == 4
    assert shift_code._meta.get_field('friday_duration').decimal_places == 2
    assert shift_code._meta.get_field('friday_duration').max_digits == 4
    assert shift_code._meta.get_field('saturday_duration').decimal_places == 2
    assert shift_code._meta.get_field('saturday_duration').max_digits == 4
    assert shift_code._meta.get_field('sunday_duration').decimal_places == 2
    assert shift_code._meta.get_field('sunday_duration').max_digits == 4
    assert shift_code._meta.get_field('stat_duration').decimal_places == 2
    assert shift_code._meta.get_field('stat_duration').max_digits == 4

def test__shift_code__role_choices(shift_code):
    """Tests the ShiftCode role choices."""
    choices = shift_code._meta.get_field('role').choices

    assert ('a', 'Pharmacy Assistant') in choices
    assert ('p', 'Pharmacist') in choices
    assert ('t', 'Pharmacy Technician') in choices

def test__shift_code__null_field_model_creation():
    """Tests ShiftCode blank fields."""
    try:
        models.ShiftCode.objects.create(code='A1', role='p')
    except IntegrityError:
        assert False
    else:
        assert True

def test__shift_code__unique_together_validation(user):
    """Tests unique validation of ShiftCode."""
    try:
        models.ShiftCode.objects.create(code='A1', sb_user=user, role='p')
        models.ShiftCode.objects.create(code='A1', sb_user=user, role='p')
    except IntegrityError:
        assert True
    else:
        assert False

def test__shift_code__str__with_user(shift_code):
    """Tests ShiftCode __str__  method with a user."""
    assert str(shift_code) == '{} - {} - {}'.format(
        shift_code.get_role_display(), shift_code.sb_user, shift_code.code
    )

def test__shift_code__str__without_user():
    """Tests ShiftCode __str__  method without a user."""
    shift_code = models.ShiftCode.objects.create(
        code='A2',
        role='p',
    )

    assert str(shift_code) == '{} - {}'.format(
        shift_code.get_role_display(), shift_code.code
    )

def test__shift__labels(shift):
    """Tests Shift labels."""
    assert shift._meta.get_field('sb_user').verbose_name == 'SB user'
    assert shift._meta.get_field('date').verbose_name == 'date'
    assert shift._meta.get_field('shift_code').verbose_name == 'shift code'
    assert shift._meta.get_field('text_shift_code').verbose_name == 'text shift code'

def test__shift__max_lengths(shift):
    """Tests Shift max_lengths."""
    assert shift._meta.get_field('text_shift_code').max_length == 20

def test__shift__str(shift):
    """Test Shift __str__ method."""
    assert str(shift) == '{} - {}'.format(shift.date, shift.shift_code)

def test__missing_shift_code__labels(missing_shift_code):
    """Test MissingShiftCode labels."""
    assert missing_shift_code._meta.get_field('code').verbose_name == 'code'
    assert missing_shift_code._meta.get_field('role').verbose_name == 'role'

def test__missing_shift_code__max_lengths(missing_shift_code):
    """Test MissingShiftCode max lengths."""
    assert missing_shift_code._meta.get_field('code').max_length == 20
    assert missing_shift_code._meta.get_field('role').max_length == 1

def test__missing_shift_code__role_choices(missing_shift_code):
    """Test MissingShiftCode role choices."""
    choices = missing_shift_code._meta.get_field('role').choices

    assert ('a', 'Pharmacy Assistant') in choices
    assert ('p', 'Pharmacist') in choices
    assert ('t', 'Pharmacy Technician') in choices

def test__missing_shift_code__str(missing_shift_code):
    """Test MissingShiftCode __str__ method."""
    assert str(missing_shift_code) == '{} - {}'.format(
        missing_shift_code.code, missing_shift_code.role
    )
