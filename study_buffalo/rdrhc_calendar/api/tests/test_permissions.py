"""Tests for the permissions module."""
from django.test import TestCase

from rdrhc_calendar.api.permissions import HasAPIAccess

class MockRequest():
    class MockUser():
        def has_perm(self, code_name):
            return True

        def __init__(self):
            pass

    def __init__(self):
        self.user = self.MockUser()

class TestHasAPIAccess(TestCase):
    def setUp(self):
        self.request = MockRequest()

    def test_has_permissions(self):
        permission = HasAPIAccess()

        self.assertTrue(permission.has_permission(self.request, ''))
