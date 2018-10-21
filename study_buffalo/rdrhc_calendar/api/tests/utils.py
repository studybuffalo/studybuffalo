"""Utility functions for the RDRHC Calendar API tests."""
from uuid import uuid4

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from rest_framework.authtoken.models import Token

from rdrhc_calendar.models import (
    CalendarUser, Shift, ShiftCode, StatHoliday
)


def create_user_without_permission(username):
    user = get_user_model().objects.create()
    user.username = username
    user.set_password('abcd123456')
    user.is_superuser = False
    user.is_staff = False
    user.is_active = True
    user.save()

    # Add a calendar user
    random_string = str(uuid4())[:10]

    CalendarUser.objects.create(
        sb_user=user,
        name=username,
        schedule_name='schedule_{}'.format(random_string),
        calendar_name='calendar_{}'.format(random_string),
        role='p',
    )

    # Add email for user
    EmailAddress.objects.create(
        user=user,
        email='{}@email.com'.format(random_string),
    )

    # Add shifts and shiftcodes for user
    shift_code = ShiftCode.objects.create(
        code='A1', sb_user=user, role='p',
        monday_start='01:00:00', monday_duration='1.1',
        tuesday_start='02:00:00', tuesday_duration='2.2',
        wednesday_start='03:00:00', wednesday_duration='3.3',
        thursday_start='04:00:00', thursday_duration='4.4',
        friday_start='05:00:00', friday_duration='5.5',
        saturday_start='06:00:00', saturday_duration='6.6',
        sunday_start='07:00:00', sunday_duration='7.7',
        stat_start='08:00:00', stat_duration='8.8',
    )

    Shift.objects.create(
        sb_user=user,
        date='2018-01-01',
        shift_code=shift_code,
        text_shift_code='A1',
    )

    Shift.objects.create(
        sb_user=user,
        date='2018-01-01',
        shift_code=None,
        text_shift_code='A2',
    )

    return user

def create_user_with_permission(username):
    # Create user
    user = create_user_without_permission(username)

    # Add permission
    content_type = ContentType.objects.get_for_model(CalendarUser)
    user.user_permissions.add(
        Permission.objects.get(content_type=content_type, codename='access_api')
    )

    # Add token
    Token.objects.get_or_create(user=user)

    return user

def create_stat_holidays():
    StatHoliday.objects.create(date='2011-01-01')
    StatHoliday.objects.create(date='2012-02-02')
    StatHoliday.objects.create(date='2013-03-03')
    StatHoliday.objects.create(date='2014-04-04')
    StatHoliday.objects.create(date='2015-05-05')
    StatHoliday.objects.create(date='2016-06-06')
    StatHoliday.objects.create(date='2017-07-07')
    StatHoliday.objects.create(date='2018-08-08')
    StatHoliday.objects.create(date='2019-09-09')
    StatHoliday.objects.create(date='2020-10-10')
