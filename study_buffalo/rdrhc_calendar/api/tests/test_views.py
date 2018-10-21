"""Tests for the RDRHC Calendar API views."""
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient, force_authenticate

from rdrhc_calendar.api import views
from rdrhc_calendar.api.tests import utils
from rdrhc_calendar.models import CalendarUser, ShiftCode


class TestAPIRoot(TestCase):
    def setUp(self):
        self.user_without_permissions = utils.create_user_without_permission(
            'user_without_permissions'
        )
        self.user = utils.create_user_with_permission('user')

    def test_403_response_on_anonymous_user(self):
        response = self.client.get(reverse('rdrhc_calendar:api_v1:root'))

        self.assertEqual(response.status_code, 403)

    def test_403_response_on_user_without_permissions(self):
        self.client.login(username='user_without_permissions', password="abcd123456")

        response = self.client.get(reverse('rdrhc_calendar:api_v1:root'))

        self.assertEqual(response.status_code, 403)

    def test_200_response_on_user_without_permissions(self):
        self.client.login(username='user', password="abcd123456")

        response = self.client.get(reverse('rdrhc_calendar:api_v1:root'))

        self.assertEqual(response.status_code, 200)

    def test_accessible_by_url(self):
        self.client.login(username='user', password="abcd123456")

        response = self.client.get('/rdrhc-calendar/api/v1/')

        self.assertEqual(response.status_code, 200)

    def test_accessible_by_token_authentication(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token {}'.format(
            self.user.auth_token.key
        ))
        response = client.get(reverse('rdrhc_calendar:api_v1:root'))
        self.assertEqual(response.status_code, 200)

class TestUserList(TestCase):
    def setUp(self):
        self.user_without_permissions = utils.create_user_without_permission(
            'user_without_permissions'
        )
        self.user = utils.create_user_with_permission('user')

    def test_403_response_on_anonymous_user(self):
        response = self.client.get(reverse('rdrhc_calendar:api_v1:user_list'))

        self.assertEqual(response.status_code, 403)

    def test_403_response_on_user_without_permissions(self):
        self.client.login(username='user_without_permissions', password="abcd123456")

        response = self.client.get(reverse('rdrhc_calendar:api_v1:user_list'))

        self.assertEqual(response.status_code, 403)

    def test_200_response_on_user_without_permissions(self):
        self.client.login(username='user', password="abcd123456")

        response = self.client.get(reverse('rdrhc_calendar:api_v1:user_list'))

        self.assertEqual(response.status_code, 200)

    def test_accessible_by_url(self):
        self.client.login(username='user', password="abcd123456")

        response = self.client.get('/rdrhc-calendar/api/v1/users/')

        self.assertEqual(response.status_code, 200)

    def test_accessible_by_token_authentication(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token {}'.format(
            self.user.auth_token.key
        ))
        response = client.get(reverse('rdrhc_calendar:api_v1:user_list'))
        self.assertEqual(response.status_code, 200)

    def test_api_returns_user_list(self):
        # Create calendar user to test response
        self.client.login(username='user', password="abcd123456")

        response = self.client.get(reverse('rdrhc_calendar:api_v1:user_list'))

        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            dict(response.data[1]),
            {
                'id': self.user.calendar_user.id,
                'sb_user': self.user.id,
                'name': self.user.calendar_user.name,
                'schedule_name': self.user.calendar_user.schedule_name,
                'calendar_name': self.user.calendar_user.calendar_name,
                'role': 'p',
                'first_email_sent': False,
                'full_day': False,
                'reminder': None,
            }
        )

class TestUserDetail(TestCase):
    def setUp(self):
        self.user_without_permissions = utils.create_user_without_permission(
            'user_without_permissions'
        )
        self.user = utils.create_user_with_permission('user')
        self.valid_args = {'user_id': self.user.calendar_user.id}
        self.valid_url = '/rdrhc-calendar/api/v1/users/{}/'.format(self.user.calendar_user.id)

    def test_403_response_on_anonymous_user(self):
        response = self.client.get(
            reverse('rdrhc_calendar:api_v1:user_detail', kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 403)

    def test_403_response_on_user_without_permissions(self):
        self.client.login(username='user_without_permissions', password="abcd123456")

        response = self.client.get(
            reverse('rdrhc_calendar:api_v1:user_detail', kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 403)

    def test_200_response_on_user_without_permissions(self):
        self.client.login(username='user', password="abcd123456")

        response = self.client.get(
            reverse('rdrhc_calendar:api_v1:user_detail', kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 200)

    def test_accessible_by_url(self):
        self.client.login(username='user', password="abcd123456")

        response = self.client.get(self.valid_url)

        self.assertEqual(response.status_code, 200)

    def test_accessible_by_token_authentication(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token {}'.format(
            self.user.auth_token.key
        ))
        response = client.get(
            reverse('rdrhc_calendar:api_v1:user_detail', kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 200)

    def test_api_returns_user_detail(self):
        self.client.login(username='user', password="abcd123456")

        response = self.client.get(
            reverse('rdrhc_calendar:api_v1:user_detail', kwargs=self.valid_args)
        )

        self.assertEqual(
            response.data,
            {
                'id': self.user.calendar_user.id,
                'sb_user': self.user.id,
                'name': self.user.calendar_user.name,
                'schedule_name': self.user.calendar_user.schedule_name,
                'calendar_name': self.user.calendar_user.calendar_name,
                'role': 'p',
                'first_email_sent': False,
                'full_day': False,
                'reminder': None,
            }
        )

class TestUserEmailList(TestCase):
    def setUp(self):
        self.user_without_permissions = utils.create_user_without_permission(
            'user_without_permissions'
        )
        self.user = utils.create_user_with_permission('user')
        self.valid_args = {'user_id': self.user.calendar_user.id}
        self.valid_url = '/rdrhc-calendar/api/v1/users/{}/emails/'.format(
            self.user.calendar_user.id
        )

    def test_403_response_on_anonymous_user(self):
        response = self.client.get(
            reverse('rdrhc_calendar:api_v1:user_email_list', kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 403)

    def test_403_response_on_user_without_permissions(self):
        self.client.login(username='user_without_permissions', password="abcd123456")

        response = self.client.get(
            reverse('rdrhc_calendar:api_v1:user_email_list', kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 403)

    def test_200_response_on_user_without_permissions(self):
        self.client.login(username='user', password="abcd123456")

        response = self.client.get(
            reverse('rdrhc_calendar:api_v1:user_email_list', kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 200)

    def test_accessible_by_url(self):
        self.client.login(username='user', password="abcd123456")

        response = self.client.get(self.valid_url)

        self.assertEqual(response.status_code, 200)

    def test_accessible_by_token_authentication(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token {}'.format(
            self.user.auth_token.key
        ))

        response = client.get(
            reverse('rdrhc_calendar:api_v1:user_email_list', kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 200)

    def test_api_returns_user_email_list(self):
        # Create calendar user to test response
        self.client.login(username='user', password="abcd123456")

        response = self.client.get(
            reverse('rdrhc_calendar:api_v1:user_email_list', kwargs=self.valid_args)
        )

        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            list(response.data),
            list(self.user.emailaddress_set.all().values_list('email', flat=True))
        )

class TestShiftList(TestCase):
    def setUp(self):
        self.user_without_permissions = utils.create_user_without_permission(
            'user_without_permissions'
        )
        self.user = utils.create_user_with_permission('user')

    def test_403_response_on_anonymous_user(self):
        response = self.client.get(reverse('rdrhc_calendar:api_v1:shift_list'))

        self.assertEqual(response.status_code, 403)

    def test_403_response_on_user_without_permissions(self):
        self.client.login(username='user_without_permissions', password="abcd123456")

        response = self.client.get(reverse('rdrhc_calendar:api_v1:shift_list'))

        self.assertEqual(response.status_code, 403)

    def test_200_response_on_user_without_permissions(self):
        self.client.login(username='user', password="abcd123456")

        response = self.client.get(reverse('rdrhc_calendar:api_v1:shift_list'))

        self.assertEqual(response.status_code, 200)

    def test_accessible_by_url(self):
        self.client.login(username='user', password="abcd123456")

        response = self.client.get('/rdrhc-calendar/api/v1/shifts/')

        self.assertEqual(response.status_code, 200)

    def test_accessible_by_token_authentication(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token {}'.format(
            self.user.auth_token.key
        ))
        response = client.get(reverse('rdrhc_calendar:api_v1:shift_list'))
        self.assertEqual(response.status_code, 200)

    def test_api_returns_shift_list(self):
        # Create calendar user to test response
        self.client.login(username='user', password="abcd123456")

        response = self.client.get(reverse('rdrhc_calendar:api_v1:shift_list'))

        self.assertEqual(len(response.data), 4)

class TestUserShiftCodeList(TestCase):
    def setUp(self):
        self.user_without_permissions = utils.create_user_without_permission(
            'user_without_permissions'
        )
        self.user = utils.create_user_with_permission('user')
        self.valid_args = {'user_id': self.user.calendar_user.id}
        self.valid_url = '/rdrhc-calendar/api/v1/shift-codes/{}/'.format(
            self.user.calendar_user.id
        )

    def test_403_response_on_anonymous_user(self):
        response = self.client.get(
            reverse('rdrhc_calendar:api_v1:user_shift_codes_list', kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 403)

    def test_403_response_on_user_without_permissions(self):
        self.client.login(username='user_without_permissions', password="abcd123456")

        response = self.client.get(
            reverse('rdrhc_calendar:api_v1:user_shift_codes_list', kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 403)

    def test_200_response_on_user_without_permissions(self):
        self.client.login(username='user', password="abcd123456")

        response = self.client.get(
            reverse('rdrhc_calendar:api_v1:user_shift_codes_list', kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 200)

    def test_accessible_by_url(self):
        self.client.login(username='user', password="abcd123456")

        response = self.client.get(self.valid_url)

        self.assertEqual(response.status_code, 200)

    def test_accessible_by_token_authentication(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token {}'.format(
            self.user.auth_token.key
        ))

        response = client.get(
            reverse('rdrhc_calendar:api_v1:user_shift_codes_list', kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 200)

    def test_api_returns_user_shift_code_list(self):
        # Add a default shift code
        shift_code = ShiftCode.objects.create(
            code='B1', sb_user=None, role='p',
            monday_start='01:00:00', monday_duration='1.1',
            tuesday_start='02:00:00', tuesday_duration='2.2',
            wednesday_start='03:00:00', wednesday_duration='3.3',
            thursday_start='04:00:00', thursday_duration='4.4',
            friday_start='05:00:00', friday_duration='5.5',
            saturday_start='06:00:00', saturday_duration='6.6',
            sunday_start='07:00:00', sunday_duration='7.7',
            stat_start='08:00:00', stat_duration='8.8',
        )

        # Create calendar user to test response
        self.client.login(username='user', password="abcd123456")

        response = self.client.get(
            reverse('rdrhc_calendar:api_v1:user_shift_codes_list', kwargs=self.valid_args)
        )

        self.assertEqual(len(response.data), 2)
