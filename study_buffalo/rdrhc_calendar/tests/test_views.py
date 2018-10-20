"""Tests for the rdrhc_calendar views."""
from django.test import TestCase
from django.urls import reverse

from rdrhc_calendar import models, views

from . import utils


class TestCalendarIndex(TestCase):
    def setUp(self):
        self.user_without_permission = utils.create_user('user_without_permission')
        self.user = utils.create_user_with_permission('user')

    def test_302_response_if_not_logged_in(self):
        response = self.client.get(reverse('rdrhc_calendar:index'))

        self.assertEqual(response.status_code, 302)

    def test_403_response_if_not_authorized(self):
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

class TestCalendarSettings(TestCase):
    def setUp(self):
        self.valid_data = {
            'calendar_name': 'SecretCalendar',
            'full_day': False,
            'reminder': '',
        }
        self.user_without_permission = utils.create_user(
            'user_without_permission'
        )
        self.user_without_calendar = utils.create_user_with_permission(
            'user_without_calendar'
        )
        self.user = utils.create_user_with_permission_calendar('user')

    def test_302_response_if_not_logged_in(self):
        response = self.client.get(reverse('rdrhc_calendar:settings'))

        self.assertEqual(response.status_code, 302)

    def test_403_response_if_not_authorized(self):
        self.client.login(
            username='user_without_permission',
            password='abcd123456'
        )
        response = self.client.get(reverse('rdrhc_calendar:settings'))

        self.assertEqual(response.status_code, 403)

    def test_404_response_if_authorized_but_no_calendar(self):
        self.client.login(
            username='user_without_calendar',
            password='abcd123456'
        )
        response = self.client.get(reverse('rdrhc_calendar:settings'))

        self.assertEqual(response.status_code, 404)

    def test_200_response_if_authorized(self):
        self.client.login(username='user', password='abcd123456')
        response = self.client.get(reverse('rdrhc_calendar:settings'))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        self.assertEqual(response.status_code, 200)

    def test_settings_url_exists_at_desired_location(self):
        self.client.login(username='user', password='abcd123456')
        response = self.client.get('/rdrhc-calendar/settings/')

        self.assertEqual(response.status_code, 200)

    def test_settings_template(self):
        self.client.login(username='user', password='abcd123456')
        response = self.client.get(reverse('rdrhc_calendar:settings'))

        self.assertTemplateUsed(response, 'rdrhc_calendar/calendar_settings.html')

    def test_redirect_to_settings_on_valid_post(self):
        self.client.login(username='user', password='abcd123456')
        response = self.client.post(
            reverse('rdrhc_calendar:settings'),
            self.valid_data,
            follow=True,
        )

        self.assertRedirects(response, reverse('rdrhc_calendar:settings'))

class TestShiftCodeList(TestCase):
    def setUp(self):
        self.user_without_permission = utils.create_user(
            'user_without_permission'
        )
        self.user_without_calendar = utils.create_user_with_permission(
            'user_without_calendar'
        )
        self.user = utils.create_user_with_permission_calendar('user')

    def test_302_response_if_not_logged_in(self):
        response = self.client.get(reverse('rdrhc_calendar:code_list'))

        self.assertEqual(response.status_code, 302)

    def test_403_response_if_not_authorized(self):
        self.client.login(
            username='user_without_permission',
            password='abcd123456'
        )
        response = self.client.get(reverse('rdrhc_calendar:code_list'))

        self.assertEqual(response.status_code, 403)

    def test_404_response_if_authorized_but_no_calendar(self):
        self.client.login(
            username='user_without_calendar',
            password='abcd123456'
        )
        response = self.client.get(reverse('rdrhc_calendar:code_list'))

        self.assertEqual(response.status_code, 404)

    def test_200_response_if_authorized(self):
        self.client.login(username='user', password='abcd123456')
        response = self.client.get(reverse('rdrhc_calendar:code_list'))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        self.assertEqual(response.status_code, 200)

    def test_settings_url_exists_at_desired_location(self):
        self.client.login(username='user', password='abcd123456')
        response = self.client.get('/rdrhc-calendar/shifts/')

        self.assertEqual(response.status_code, 200)

    def test_settings_template(self):
        self.client.login(username='user', password='abcd123456')
        response = self.client.get(reverse('rdrhc_calendar:code_list'))

        self.assertTemplateUsed(response, 'rdrhc_calendar/shiftcode_list.html')

class TestCalendarCodeEdit(TestCase):
    def setUp(self):
        self.user_without_permission = utils.create_user(
            'user_without_permission'
        )
        self.user_without_calendar = utils.create_user_with_permission(
            'user_without_calendar'
        )
        self.user = utils.create_user_with_permission_calendar('user')
        self.shift_code = models.ShiftCode.objects.create(
            code='A1',
            sb_user=self.user,
            monday_start='01:00:00',
            monday_duration='1.1',
            tuesday_start='02:00:00',
            tuesday_duration='2.2',
            wednesday_start='03:00:00',
            wednesday_duration='3.3',
            thursday_start='04:00:00',
            thursday_duration='4.4',
            friday_start='05:00:00',
            friday_duration='5.5',
            saturday_start='06:00:00',
            saturday_duration='6.6',
            sunday_start='07:00:00',
            sunday_duration='7.7',
            stat_start='08:00:00',
            stat_duration='8.8',
        )
        self.valid_data = {
            'code': 'A2',
            'monday_start': '01:00:00',
            'monday_duration': '1.1',
            'tuesday_start': '02:00:00',
            'tuesday_duration': '2.2',
            'wednesday_start': '03:00:00',
            'wednesday_duration': '3.3',
            'thursday_start': '04:00:00',
            'thursday_duration': '4.4',
            'friday_start': '05:00:00',
            'friday_duration': '5.5',
            'saturday_start': '06:00:00',
            'saturday_duration': '6.6',
            'sunday_start': '07:00:00',
            'sunday_duration': '7.7',
            'stat_start': '08:00:00',
            'stat_duration': '8.8',
        }
        self.valid_args = {'code_id': self.shift_code.id}
        self.valid_url = '/rdrhc-calendar/shifts/{}/'.format(self.shift_code.id)

    def test_302_response_if_not_logged_in(self):
        response = self.client.get(
            reverse('rdrhc_calendar:code_edit', kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_403_response_if_not_authorized(self):
        self.client.login(
            username='user_without_permission',
            password='abcd123456'
        )
        response = self.client.get(
            reverse('rdrhc_calendar:code_edit', kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 403)

    def test_404_response_if_authorized_but_no_calendar(self):
        self.client.login(
            username='user_without_calendar',
            password='abcd123456'
        )
        response = self.client.get(
            reverse('rdrhc_calendar:code_edit', kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 404)

    def test_200_response_if_authorized(self):
        self.client.login(username='user', password='abcd123456')
        response = self.client.get(
            reverse('rdrhc_calendar:code_edit', kwargs=self.valid_args)
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        self.assertEqual(response.status_code, 200)

    def test_code_list_url_exists_at_desired_location(self):
        self.client.login(username='user', password='abcd123456')
        response = self.client.get(self.valid_url)

        self.assertEqual(response.status_code, 200)

    def test_code_list_template(self):
        self.client.login(username='user', password='abcd123456')
        response = self.client.get(
            reverse('rdrhc_calendar:code_edit', kwargs=self.valid_args)
        )

        self.assertTemplateUsed(response, 'rdrhc_calendar/shiftcode_edit.html')

    def test_redirect_to_code_list_on_valid_post(self):
        self.client.login(username='user', password='abcd123456')
        response = self.client.post(
            reverse('rdrhc_calendar:code_edit', kwargs=self.valid_args),
            self.valid_data,
            follow=True
        )

        self.assertRedirects(response, reverse('rdrhc_calendar:code_list'))
