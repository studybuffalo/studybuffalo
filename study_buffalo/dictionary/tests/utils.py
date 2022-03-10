"""Utility functions for testing Dictionary app."""
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from dictionary.models import WordPending


def add_view_permission(user):
    """Adds the 'can_view' permission to the provided user."""
    content_type = ContentType.objects.get_for_model(WordPending)
    user.user_permissions.add(
        Permission.objects.get(content_type=content_type, codename='can_view')
    )
