"""Tests for the rdrhc_calendar models."""
from django.apps import AppConfig
from django.conf import settings
from django.test import TestCase

from rdrhc_calendar import models


def create_user():
    user = AppConfig.get_model('users', settings.AUTH_USER_MODEL).objects.create()
    user.username = 'Regular User'
    user.set_password('abcd123456')
    user.is_superuser = False
    user.is_staff = False
    user.is_active = True
    user.save()

    return user

class CalendarUserTest(TestCase):
    def setUp(self):
        self.calendar_user = models.CalendarUser.objects.create(
            sb_user=create_user(),
            name='Regular User',
            schedule_name='User',
            calendar_name='SecretCalendar',
            role='p',
            first_email_sent=False,
            full_day=False,
            reminder=0,
        )

    def test_labels(self):
        self.assertEqual(
            self.base_abstract._meta.get_field('id').verbose_name,
            'id',
        )
