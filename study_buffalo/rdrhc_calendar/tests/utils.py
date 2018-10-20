"""Utility functions for testing."""
from django.contrib.auth import get_user_model

def create_user(username):
    user = get_user_model().objects.create()
    user.username = username
    user.set_password('abcd123456')
    user.is_superuser = False
    user.is_staff = False
    user.is_active = True
    user.save()

    return user
