"""Utility functions for testing Substitutions app."""
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from substitutions.models import Apps


def add_view_permission(user):
    """Adds the 'can_view' permission to the provided user."""
    content_type = ContentType.objects.get_for_model(Apps)
    user.user_permissions.add(
        Permission.objects.get(content_type=content_type, codename='can_view')
    )
