from django.urls import reverse
from django.test import TestCase

from .utils import create_user

class APIRootTest(TestCase):
    def setUp(self):
        self.user = create_user()

    def test_v1_root_url_exists(self):
        '''Checks that the API root uses the correct URL'''
        self.client.login(username=self.user.username, password='abcd123456')
        response = self.client.get('/flash-cards/api/v1/')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_v1_root_accessible_by_name(self):
        '''Checks that the dashboard URL name works properly'''
        self.client.login(username=self.user.username, password='abcd123456')
        response = self.client.get(reverse("flash_cards:api_v1:root"))

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
