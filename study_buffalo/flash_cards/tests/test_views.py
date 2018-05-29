from django.urls import reverse

from django.test import TestCase

from .utils import create_user

class APIRootTest(TestCase):
    def setUp(self):
        self.user = create_user()

    def test_403_on_anonymous_user(self):
        response = self.client.get(reverse('flash_cards:api_v1:root'))

        # Check that proper error code returned
        self.assertEqual(response.status_code, 403)

    def test_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get(reverse("flash_cards:api_v1:root"))

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_exists_at_proper_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get("/flash_cards/api/v1/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

class CardListTest(TestCase):
    def setUp(self):
        self.user = create_user()

    def test_403_on_anonymous_user(self):
        response = self.client.get(reverse('flash_cards:api_v1:card_list'))

        # Check that proper error code returned
        self.assertEqual(response.status_code, 403)

    def test_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get(reverse("flash_cards:api_v1:card_list"))

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_exists_at_proper_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get("/flash_cards/api/v1/card-list/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_get_retrieves_cards(self):
        pass

    def test_post_adds_card(self):
        pass

    def test_post_response(self):
        pass

    def test_post_error(self):
        pass

class DeckListTest(TestCase):
    def setUp(self):
        self.user = create_user()

    def test_403_on_anonymous_user(self):
        response = self.client.get(reverse('flash_cards:api_v1:deck_list'))

        # Check that proper error code returned
        self.assertEqual(response.status_code, 403)

    def test_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get(reverse("flash_cards:api_v1:deck_list"))

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_exists_at_proper_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get("/flash_cards/api/v1/deck-list/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_get_retrieves_decks(self):
        pass

    def test_post_adds_deck(self):
        pass

    def test_post_response(self):
        pass

    def test_post_error(self):
        pass

class TagListTest(TestCase):
    def setUp(self):
        self.user = create_user()

    def test_403_on_anonymous_user(self):
        response = self.client.get(reverse('flash_cards:api_v1:tag_list'))

        # Check that proper error code returned
        self.assertEqual(response.status_code, 403)

    def test_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get(reverse("flash_cards:api_v1:tag_list"))

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_exists_at_proper_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get("/flash_cards/api/v1/tag-list/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

class TagDetailTest(TestCase):
    def setUp(self):
        self.user = create_user()

    def test_403_on_anonymous_user(self):
        response = self.client.get(reverse('flash_cards:api_v1:tag_list'))

        # Check that proper error code returned
        self.assertEqual(response.status_code, 403)

    def test_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get(reverse("flash_cards:api_v1:tag_list"))

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_exists_at_proper_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get("/flash_cards/api/v1/tag-list/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
