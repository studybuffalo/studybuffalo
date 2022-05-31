"""Utility functions for testing."""
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from hc_dpd.models import DPD


def add_web_view_permission(user):
    """Adds the 'web_view' permission to the provided user."""
    content_type = ContentType.objects.get_for_model(DPD)
    user.user_permissions.add(
        Permission.objects.get(content_type=content_type, codename='web_view')
    )
