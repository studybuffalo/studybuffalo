"""Tests for the rdrhc_calendar views."""
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse


from rdrhc_calendar import models, views

from .utils import create_user

class TestCalendarIndex(TestCase):
    def setUp(self):
        self.user_without_permission = create_user('user_without_permission')
        self.user = create_user('user')

        # Add permission to user
        content_type = ContentType.objects.get_for_model(models.CalendarUser)
        self.user.user_permissions.add(
            Permission.objects.get(content_type=content_type, codename='can_view')
        )

    def test_403_response_if_not_authorized(self):
        response = self.client.get(reverse('rdrhc_calendar:index'))

        self.assertEqual(response.status_code, 403)

    def test_403_response_if_not_authorized_and_logged_in(self):
        self.client.login(
            username='user_without_permission',
            password='abcd123456'
        )
        response = self.client.get(reverse('rdrhc_calendar:index'))

        self.assertEqual(response.status_code, 403)

    def test_200_response_if_authorized(self):
        self.client.login(username='user', password='abcd123456')
        response = self.client.get(reverse('rdrhc_calendar:index'))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        self.assertEqual(response.status_code, 200)

    def test_index_url_exists_at_desired_location(self):
        self.client.login(username='user', password='abcd123456')
        response = self.client.get('/rdrhc-calendar/')

        self.assertEqual(response.status_code, 200)

    def test_index_template(self):
        self.client.login(username='user', password='abcd123456')
        response = self.client.get(reverse('rdrhc_calendar:index'))

        self.assertTemplateUsed(response, 'rdrhc_calendar/index.html')
