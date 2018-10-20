"""Utility functions for testing."""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from rdrhc_calendar import models


def create_user(username):
    user = get_user_model().objects.create()
    user.username = username
    user.set_password('abcd123456')
    user.is_superuser = False
    user.is_staff = False
    user.is_active = True
    user.save()

    return user

def create_user_with_permission(username):
    # Create user
    user = create_user(username)

    # Add permission
    content_type = ContentType.objects.get_for_model(models.CalendarUser)
    user.user_permissions.add(
        Permission.objects.get(content_type=content_type, codename='can_view')
    )

    return user

def create_user_with_permission_calendar(username):
    # Create user
    user = create_user(username)

    # Add permission
    content_type = ContentType.objects.get_for_model(models.CalendarUser)
    user.user_permissions.add(
        Permission.objects.get(content_type=content_type, codename='can_view')
    )

    # Add CalendarUser to user
    models.CalendarUser.objects.create(
        sb_user=user,
        name='Regular User',
        schedule_name='User',
        calendar_name='SecretCalendar',
        role='p',
    )

    return user

def create_user_with_missing_shift_permission(username):
    # Create user
    user = create_user(username)

    # Add permission
    content_type = ContentType.objects.get_for_model(models.MissingShiftCode)
    user.user_permissions.add(
        Permission.objects.get(
            content_type=content_type, codename='can_add_default_codes'
        )
    )

    return user
