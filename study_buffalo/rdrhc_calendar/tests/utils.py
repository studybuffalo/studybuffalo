"""Utility functions for testing."""
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

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
        Permission.objects.get(
            content_type=content_type, codename='can_add_default_codes'
        )
    )
