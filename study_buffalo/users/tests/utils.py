"""Utility functions for testing the User app."""
from rest_framework.authtoken.models import Token


def create_token(user):
    """Creates token for provided user."""
    return Token.objects.create(user=user)
