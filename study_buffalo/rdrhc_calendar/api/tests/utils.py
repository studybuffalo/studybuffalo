"""Utility functions for the RDRHC Calendar API tests."""
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from rest_framework.authtoken.models import Token

from rdrhc_calendar.models import CalendarUser


def create_user_without_permission(username):
    user = get_user_model().objects.create()
    user.username = username
    user.set_password('abcd123456')
    user.is_superuser = False
    user.is_staff = False
    user.is_active = True
    user.save()

    random_string = str(uuid4())[:10]

    calendar_user = CalendarUser.objects.create(
        sb_user=user,
        name=username,
        schedule_name='schedule_{}'.format(random_string),
        calendar_name='calendar_{}'.format(random_string),
        role='p',
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
