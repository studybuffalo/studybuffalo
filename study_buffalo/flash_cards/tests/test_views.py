import json
from rest_framework.test import APIClient

from django.urls import reverse
from django.test import TestCase

from flash_cards import models
from flash_cards.tests import utils

class APIRootTest(TestCase):
    def setUp(self):
        self.user = utils.create_user()

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
        models.Card.objects.create()

        self.client = APIClient()
        self.user = utils.create_user()
        self.post_data = utils.create_card_post_data()

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

class CardDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = utils.create_user()
        self.card = models.Card.objects.create()
        self.post_data = utils.create_card_post_data()

    def test_403_on_anonymous_user(self):
        response = self.client.get(reverse(
            'flash_cards:api_v1:card_detail',
            kwargs={'id': self.card.id}
        ))

        # Check that proper error code returned
        self.assertEqual(response.status_code, 403)

    def test_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get(reverse(
            'flash_cards:api_v1:card_detail',
            kwargs={'id': self.card.id}
        ))

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_accessible_by_url(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get(
            "/flash-cards/api/v1/cards/{}/".format(self.card.id)
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_get_retrieves_card(self):
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get(
            reverse(
                'flash_cards:api_v1:card_detail',
                kwargs={'id': self.card.id}
            ),
            format='json'
        )
        json_response = json.loads(response.content)

        # Check that proper card is retrieved
        self.assertEqual(json_response['id'], str(self.card.id))

    def test_put_response(self):
        # Use POST data to create a card entry
        self.client.login(username=self.user.username, password="abcd123456")
        post_response = self.client.post(
            reverse("flash_cards:api_v1:card_list"),
            self.post_data,
            format='json'
        )
        card_id = json.loads(post_response.content)['id']

        # Get current model counts
        card_count = models.Card.objects.all().count()
        question_count = models.QuestionPart.objects.all().count()
        answer_count = models.FreeformAnswerPart.objects.all().count()
        rationale_count = models.RationalePart.objects.all().count()
        reference_count = models.Reference.objects.all().count()

        # Modify data to test PUT requets
        put_data = self.post_data
        put_data['reviewed'] = True
        put_data['date_reviewed'] = '2018-06-01T12:00:00.000000Z'

        # Make the PUT request
        response = self.client.put(
            reverse(
                'flash_cards:api_v1:card_detail',
                kwargs={'id': card_id}
            ),
            put_data,
            format='json'
        )
        json_response = json.loads(response.content)

        # Confirm modified response code
        self.assertEqual(response.status_code, 200)

        # Confirm same ID returned
        self.assertEqual(json_response['id'], card_id)

        # Confirm model counts remained the same
        self.assertEqual(
            models.Card.objects.all().count(),
            card_count
        )
        self.assertEqual(
            models.QuestionPart.objects.all().count(),
            question_count
        )
        self.assertEqual(
            models.FreeformAnswerPart.objects.all().count(),
            answer_count
        )
        self.assertEqual(
            models.RationalePart.objects.all().count(),
            rationale_count
        )
        self.assertEqual(
            models.Reference.objects.all().count(),
            reference_count
        )

    def test_put_error(self):
        # Use POST data to create a card entry
        self.client.login(username=self.user.username, password="abcd123456")
        post_response = self.client.post(
            reverse("flash_cards:api_v1:card_list"),
            self.post_data,
            format='json'
        )
        card_id = json.loads(post_response.content)['id']

        # Modify data to test PUT requets
        put_data = self.post_data
        put_data['active'] = None

        # Make the PUT request
        response = self.client.put(
            reverse(
                'flash_cards:api_v1:card_detail',
                kwargs={'id': card_id}
            ),
            put_data,
            format='json'
        )
        json_response = json.loads(response.content)

        # Confirm modified response code
        self.assertEqual(response.status_code, 400)

        # Confirm this was expected error
        self.assertCountEqual(json_response, ['active'])
        self.assertEqual(
            json_response['active'],
            ['This field may not be null.']
        )

    def test_delete(self):
        # Use POST data to create a card entry
        self.client.login(username=self.user.username, password="abcd123456")
        post_response = self.client.post(
            reverse("flash_cards:api_v1:card_list"),
            self.post_data,
            format='json'
        )
        card_id = json.loads(post_response.content)['id']

        # Get current model counts
        card_count = models.Card.objects.all().count()
        question_count = models.QuestionPart.objects.all().count()
        answer_count = models.FreeformAnswerPart.objects.all().count()
        rationale_count = models.RationalePart.objects.all().count()
        reference_count = models.Reference.objects.all().count()

        delete_response = self.client.delete(
            reverse(
                'flash_cards:api_v1:card_detail',
                kwargs={'id': card_id}
            ),
            format='json'
        )

        # Confirm status code
        self.assertEqual(delete_response.status_code, 204)

        # Confirm deletions
        self.assertEqual(
            models.Card.objects.all().count(),
            card_count - 1
        )
        self.assertEqual(
            models.QuestionPart.objects.all().count(),
            question_count - 1
        )
        self.assertEqual(
            models.FreeformAnswerPart.objects.all().count(),
            answer_count - 2
        )
        self.assertEqual(
            models.RationalePart.objects.all().count(),
            rationale_count - 1
        )
        self.assertEqual(
            models.Reference.objects.all().count(),
            reference_count - 1
        )

class DeckListTest(TestCase):
    def setUp(self):
        # Populate database with values
        models.Deck.objects.create(deck_name='Neurology Deck')

        self.client = APIClient()
        self.user = utils.create_user()
        self.post_data = utils.create_deck_post_data()

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
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get(reverse("flash_cards:api_v1:deck_list"))

        json_response = json.loads(response.content)

        self.assertEqual(len(json_response), 1)

    def test_post_adds_deck(self):
        # Count current number of cards
        deck_total = models.Deck.objects.all().count()

        # POST data and retrieve response
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.post(
            reverse("flash_cards:api_v1:deck_list"),
            self.post_data,
            format='json'
        )

        # Confirm proper status code
        self.assertEqual(response.status_code, 201)

        # Check that a card was added
        self.assertEqual(
            models.Deck.objects.all().count(),
            deck_total + 1
        )

    def test_post_response(self):
        # POST data and retrieve response
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.post(
            reverse("flash_cards:api_v1:deck_list"),
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
        # Remove deck name
        data = self.post_data
        data.pop('deck_name')

        # POST data and retrieve response
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.post(
            reverse("flash_cards:api_v1:deck_list"),
            data,
            format='json'
        )
        json_response = json.loads(response.content)

        # Check for an error status code
        self.assertEqual(response.status_code, 400)

        # Confirm this was expected error
        self.assertCountEqual(json_response, ['deck_name'])
        self.assertEqual(
            json_response['deck_name'],
            ['This field is required.']
        )

class DeckDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = utils.create_user()
        self.deck = models.Deck.objects.create(deck_name='Urology Deck')
        self.post_data = {
            'deck_name': 'Neurology Deck',
        }

    def test_403_on_anonymous_user(self):
        response = self.client.get(reverse(
            'flash_cards:api_v1:deck_detail',
            kwargs={'id': self.deck.id}
        ))

        # Check that proper error code returned
        self.assertEqual(response.status_code, 403)

    def test_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get(reverse(
            'flash_cards:api_v1:deck_detail',
            kwargs={'id': self.deck.id}
        ))

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_accessible_by_url(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get(
            "/flash-cards/api/v1/decks/{}/".format(self.deck.id)
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_get_retrieves_deck(self):
        self.client.login(username=self.user.username, password="abcd123456")
        response = self.client.get(
            reverse(
                'flash_cards:api_v1:deck_detail',
                kwargs={'id': self.deck.id}
            ),
            format='json'
        )
        json_response = json.loads(response.content)

        # Check that proper card is retrieved
        self.assertEqual(json_response['id'], str(self.deck.id))

    def test_put_response(self):
        # Use POST data to create a deck entry
        self.client.login(username=self.user.username, password="abcd123456")
        post_response = self.client.post(
            reverse("flash_cards:api_v1:deck_list"),
            self.post_data,
            format='json'
        )

        deck_id = json.loads(post_response.content)['id']

        # Get current deck count
        deck_count = models.Deck.objects.all().count()

        # Modify data to test PUT requets
        put_data = self.post_data
        put_data['deck_name'] = 'Tobacco Cessation'

        # Make the PUT request
        response = self.client.put(
            reverse(
                'flash_cards:api_v1:deck_detail',
                kwargs={'id': deck_id}
            ),
            put_data,
            format='json'
        )
        json_response = json.loads(response.content)

        # Confirm modified response code
        self.assertEqual(response.status_code, 200)

        # Confirm same ID returned
        self.assertEqual(json_response['id'], deck_id)

        # Confirm model counts remained the same
        self.assertEqual(
            models.Deck.objects.all().count(),
            deck_count
        )

    def test_put_error(self):
        # Use POST data to create a card entry
        self.client.login(username=self.user.username, password="abcd123456")
        post_response = self.client.post(
            reverse("flash_cards:api_v1:deck_list"),
            self.post_data,
            format='json'
        )
        deck_id = json.loads(post_response.content)['id']

        # Modify data to test PUT requets
        put_data = self.post_data
        put_data['deck_name'] = None

        # Make the PUT request
        response = self.client.put(
            reverse(
                'flash_cards:api_v1:deck_detail',
                kwargs={'id': deck_id}
            ),
            put_data,
            format='json'
        )
        json_response = json.loads(response.content)

        # Confirm modified response code
        self.assertEqual(response.status_code, 400)

        # Confirm this was expected error
        self.assertCountEqual(json_response, ['deck_name'])
        self.assertEqual(
            json_response['deck_name'],
            ['This field may not be null.']
        )

    def test_delete(self):
        # Use POST data to create a card entry
        self.client.login(username=self.user.username, password="abcd123456")
        post_response = self.client.post(
            reverse("flash_cards:api_v1:deck_list"),
            self.post_data,
            format='json'
        )
        deck_id = json.loads(post_response.content)['id']

        # Get current model counts
        deck_count = models.Deck.objects.all().count()

        delete_response = self.client.delete(
            reverse(
                'flash_cards:api_v1:deck_detail',
                kwargs={'id': deck_id}
            ),
            format='json'
        )

        # Confirm status code
        self.assertEqual(delete_response.status_code, 204)

        # Confirm deletions
        self.assertEqual(
            models.Deck.objects.all().count(),
            deck_count - 1
        )

class TagListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = utils.create_user()

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

    def test_get_retrieves_tags(self):
        pass

    def test_post_adds_deck(self):
        pass

    def test_post_response(self):
        pass

    def test_post_error(self):
        pass

class TagDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = utils.create_user()

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

    def test_put_response(self):
        pass

    def test_put_error(self):
        pass

    def test_delete(self):
        pass
