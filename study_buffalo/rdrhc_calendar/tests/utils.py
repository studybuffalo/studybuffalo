"""Utility functions for testing."""
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from rest_framework.authtoken.models import Token

from rdrhc_calendar.models import CalendarUser, MissingShiftCode


def add_view_permission(user):
    """Adds the 'can_view' permission to the provided user."""
    content_type = ContentType.objects.get_for_model(CalendarUser)
    user.user_permissions.add(
        Permission.objects.get(content_type=content_type, codename='can_view')
    )

def add_add_default_codes_permissions(user):
    """Adds the 'can_add_default_codes' permission to the provided user."""
    content_type = ContentType.objects.get_for_model(MissingShiftCode)
    user.user_permissions.add(
        Permission.objects.get(content_type=content_type, codename='can_add_default_codes')
    )

def add_api_permission(user):
    """Addss the 'access_api' permission to the provided user."""
    content_type = ContentType.objects.get_for_model(CalendarUser)
    user.user_permissions.add(
        Permission.objects.get(content_type=content_type, codename='access_api')
    )

def create_token(user):
    """Creates token for provided user."""
    return Token.objects.create(user=user)

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
