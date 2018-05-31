import json
from rest_framework.test import APIClient

from django.urls import reverse
from django.test import TestCase

from flash_cards import models

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

    def test_accessible_by_url(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get("/flash-cards/api/v1/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

class CardListTest(TestCase):
    def setUp(self):
        # Populate database with values
        deck = models.Deck.objects.create(deck_name='Cardiology Study Deck')
        tag = models.Tag.objects.create(tag_name='cardiology')
        models.Card.objects.create()
        models.Synonym.objects.create(tag=tag, synonym_name='cardiology')

        self.client = APIClient()
        self.user = create_user()
        self.post_data = {
            'question_parts': [
                {
                    'order': 1,
                    'media_type': 't',
                    'text': 'This is question text',
                    'media': None,
                },
            ],
            'freeform_answer_parts': [
                {
                    'order': 1,
                    'media_type': 't',
                    'text': 'This is freeform answer text',
                    'media': None,
                },
                {
                    'order': 2,
                    'media_type': 't',
                    'text': 'This is some more text',
                    'media': None,
                },
            ],
            'rationale_parts': [
                {
                    'order': 1,
                    'media_type': 't',
                    'text': 'This is rationale text',
                    'media': None,
                },
            ],
            'reviewed': False,
            'active': True,
            'date_modified': '2018-01-01T12:00:00.000000Z',
            'date_reviewed': '2018-01-02T12:00:00.000000Z',
            'references': [
                {'reference': 'This is reference text'},
            ],
            'decks': [
                {'id': deck.id},
            ],
            'tags': [
                {'tag_name': tag.tag_name},
            ],
        }

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

    def test_accessible_by_url(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get("/flash-cards/api/v1/cards/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_get_retrieves_cards(self):
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get(reverse("flash_cards:api_v1:card_list"))

        json_response = json.loads(response.content)

        self.assertEqual(len(json_response), 1)

    def test_post_adds_card(self):
        # Count current number of cards
        card_total = models.Card.objects.all().count()

        # POST data and retrieve response
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.post(
            reverse("flash_cards:api_v1:card_list"),
            self.post_data,
            format='json'
        )

        # Confirm proper status code
        self.assertEqual(response.status_code, 201)

        # Check that a card was added
        self.assertEqual(
            models.Card.objects.all().count(),
            card_total + 1
        )

    def test_post_response(self):
        # POST data and retrieve response
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.post(
            reverse("flash_cards:api_v1:card_list"),
            self.post_data,
            format='json'
        )
        json_response = json.loads(response.content)

        # Confirm proper status code
        self.assertEqual(response.status_code, 201)

        # Check that response has a UUID
        self.assertTrue('id' in json_response)
        self.assertTrue(json_response['id'])

    def test_post_error(self):
        # Remove question_parts
        data = self.post_data
        data.pop('question_parts')

        # POST data and retrieve response
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.post(
            reverse("flash_cards:api_v1:card_list"),
            self.post_data,
            format='json'
        )
        json_response = json.loads(response.content)

        # Check for an error status code
        self.assertEqual(response.status_code, 400)

        # Confirm this was expected error
        self.assertCountEqual(json_response, ['question_parts'])
        self.assertEqual(
            json_response['question_parts'],
            ['This field is required.']
        )

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

    def test_accessible_by_url(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get("/flash-cards/api/v1/decks/")

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

    def test_accessible_by_url(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get("/flash-cards/api/v1/tags/")

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

    def test_accessible_by_url(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get("/flash-cards/api/v1/tags/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
