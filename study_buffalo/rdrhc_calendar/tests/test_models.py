"""Tests for the rdrhc_calendar models."""
from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.test import TestCase

from rdrhc_calendar import models


def create_user():
    user = get_user_model().objects.create()
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
            self.calendar_user._meta.get_field('id').verbose_name,
            'ID',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('sb_user').verbose_name,
            'SB user',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('name').verbose_name,
            'name',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('schedule_name').verbose_name,
            'schedule name',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('calendar_name').verbose_name,
            'calendar name',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('role').verbose_name,
            'role',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('first_email_sent').verbose_name,
            'first email sent',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('full_day').verbose_name,
            'full day',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('reminder').verbose_name,
            'reminder',
        )
