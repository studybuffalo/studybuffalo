"""Utility functions for Drug Price Calculator testing."""
from rest_framework.authtoken.models import Token


def create_token(user):
    """Creates token for provided user."""
    return Token.objects.create(user=user)
