from django.test import TestCase

from flash_cards.models import Card, CardDeck, Tag, Synonym, CardTag, Reference
from flash_cards.serializers import (
    PartSerializer, MultipleChoiceSerializer, MatchingSerializer, AnswerSerializer,
    TagSerializer, DeckSerializer, NewCardSerializer
)

from .utils import create_deck

class PartSerializerTest(TestCase):
    def setUp(self):
        # TODO: Add tests for audio, image, and videos
        self.text_data = {
            'text': 'This is test text',
            'order': 1,
        }

    def test_accepts_valid_text_data(self):
        serializer = PartSerializer(data=self.text_data)

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = PartSerializer(self.text_data)

        self.assertCountEqual(
            serializer.data.keys(),
            ['audio', 'image', 'text', 'video', 'order']
        )

    def test_text_max_length(self):
        invalid_text_data = self.text_data
        invalid_text_data['text'] = 'a' * 2001

        serializer = PartSerializer(data=invalid_text_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the text error is present
        self.assertCountEqual(
            serializer.errors,
            ['text']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['text'],
            ['Ensure this field has no more than 2000 characters.']
        )

    def test_order_min_value(self):
        invalid_data = self.text_data
        invalid_data['order'] = 0

        serializer = PartSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the text error is present
        self.assertCountEqual(
            serializer.errors,
            ['order']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['order'],
            ['Ensure this value is greater than or equal to 1.']
        )

    # TODO: Add tests to handle custom validation for only 1 type of data

class MultipleChoiceSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            'content': [
                {
                    'text': 'This is test text',
                    'order': 1,
                },
            ],
            'order': 1,
            'correct': True,
        }

    def test_accepts_valid_data(self):
        serializer = MultipleChoiceSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = MultipleChoiceSerializer(self.data)

        self.assertCountEqual(
            serializer.data.keys(),
            ['content', 'order', 'correct']
        )

    def test_order_min_value(self):
        invalid_data = self.data
        invalid_data['order'] = 0

        serializer = MultipleChoiceSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the text error is present
        self.assertCountEqual(
            serializer.errors,
            ['order']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['order'],
            ['Ensure this value is greater than or equal to 1.']
        )

class MatchingSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            'content': [
                {
                    'text': 'This is test text',
                    'order': 1,
                },
            ],
            'side': 'l',
            'order': 1,
            'pair': 1,
        }

    def test_accepts_valid_data(self):
        serializer = MatchingSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = MatchingSerializer(self.data)

        self.assertCountEqual(
            serializer.data.keys(),
            ['content', 'side', 'order', 'pair']
        )

    def test_side_choice_restrictions(self):
        invalid_data = self.data
        invalid_data['side'] = 'a'

        serializer = MatchingSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the text error is present
        self.assertCountEqual(
            serializer.errors,
            ['side']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['side'],
            ['"a" is not a valid choice.']
        )

    def test_order_min_value(self):
        invalid_data = self.data
        invalid_data['order'] = 0

        serializer = MatchingSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the text error is present
        self.assertCountEqual(
            serializer.errors,
            ['order']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['order'],
            ['Ensure this value is greater than or equal to 1.']
        )

    def test_pair_min_value(self):
        invalid_data = self.data
        invalid_data['order'] = 0

        serializer = MatchingSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the text error is present
        self.assertCountEqual(
            serializer.errors,
            ['order']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['order'],
            ['Ensure this value is greater than or equal to 1.']
        )

class AnswerSerializerTest(TestCase):
    def setUp(self):
        self.multiple_choice_data = {
            'multiple_choice': [
                {
                    'content': [
                        {
                            'text': 'This is test text',
                            'order': 1,
                        },
                    ],
                    'order': 1,
                    'correct': True,
                },
            ]
        }
        self.matching_data = {
            'multiple_choice': [
                {
                    'content': [
                        {
                            'text': 'This is test text',
                            'order': 1,
                        },
                    ],
                    'side': 'l',
                    'order': 1,
                    'pair': 1,
                },
            ]
        }
        self.freeform_data = {
            'freeform': [
                {
                    'text': 'This is test text',
                    'order': 1,
                },
            ]
        }

    def test_accepts_valid_multiple_choice_data(self):
        serializer = AnswerSerializer(data=self.multiple_choice_data)

        self.assertTrue(serializer.is_valid())

    def test_accepts_valid_matching_data(self):
        serializer = AnswerSerializer(data=self.matching_data)

        self.assertTrue(serializer.is_valid())

    def test_accepts_valid_freeform_data(self):
        serializer = AnswerSerializer(data=self.freeform_data)

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = AnswerSerializer({
            'multiple_choice': [],
            'matching': [],
            'freeform': []
        })

        self.assertCountEqual(
            serializer.data.keys(),
            ['multiple_choice', 'matching', 'freeform']
        )

    def test_zero_answer_validation(self):
        serializer = AnswerSerializer(data={})

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the text error is present
        self.assertCountEqual(
            serializer.errors,
            ['non_field_errors']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['non_field_errors'],
            ['Must provide an answer.']
        )

    def test_more_than_one_answer_validation(self):
        invalid_data = {
            'multiple_choice': self.multiple_choice_data['multiple_choice'],
            'freeform': self.freeform_data['freeform']
        }

        serializer = AnswerSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the text error is present
        self.assertCountEqual(
            serializer.errors,
            ['non_field_errors']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['non_field_errors'],
            ['Must submit only one answer type.']
        )

class TagSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            'tag_name': 'cardiology'
        }

    def test_accepts_valid_data(self):
        serializer = TagSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = TagSerializer(self.data)

        self.assertCountEqual(
            serializer.data.keys(),
            ['tag_name']
        )

    def test_tag_name_max_length(self):
        invalid_text_data = self.data
        invalid_text_data['tag_name'] = 'a' * 101

        serializer = TagSerializer(data=invalid_text_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the text error is present
        self.assertCountEqual(
            serializer.errors,
            ['tag_name']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['tag_name'],
            ['Ensure this field has no more than 100 characters.']
        )

class DeckSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            'deck_uuid': '1e59d275-704f-479e-a911-ba2119f13d0d',
            'deck_name': 'Cardiology',
            'reviewed': False,
            'active': True,
            'date_modified': '2018-01-01T12:01:00.000000Z',
            'date_reviewed': '2018-02-01T12:01:00.000000Z',
        }

    def test_accepts_valid_data(self):
        serializer = DeckSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = DeckSerializer(self.data)

        self.assertCountEqual(
            serializer.data.keys(),
            ['deck_uuid', 'deck_name', 'reviewed', 'active', 'date_modified', 'date_reviewed']
        )

    def test_deck_uuid_cannot_be_set(self):
        invalid_data = self.data
        invalid_data['deck_uuid'] = '1a'

        serializer = DeckSerializer(data=invalid_data)

        # Check that serializer is valid
        self.assertTrue(serializer.is_valid())

    def test_deck_name_max_length(self):
        invalid_data = self.data
        invalid_data['deck_name'] = 'a' * 256

        serializer = DeckSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the deck_name error is present
        self.assertCountEqual(
            serializer.errors,
            ['deck_name']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['deck_name'],
            ['Ensure this field has no more than 255 characters.']
        )

    def test_invalid_date_handling(self):
        invalid_data = self.data
        invalid_data['date_reviewed'] = '2017-01-01'

        serializer = DeckSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the date_reviewed error is present
        self.assertCountEqual(
            serializer.errors,
            ['date_reviewed']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['date_reviewed'],
            [
                'Datetime has wrong format. Use one of these formats instead: '
                'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'
            ]
        )

class NewCardSerializerTest(TestCase):
    def setUp(self):
        deck = create_deck('cardiology')

        self.data = {
            'uuid': '',
            'question': [
                {
                    'text': 'This is question text part 1',
                    'order': 1,
                },
                {
                    'text': 'This is question text part 2',
                    'order': 2,
                },
            ],
            'answer': {
                'freeform': [
                    {
                        'text': 'This is answer text',
                        'order': 1,
                    },
                ]
            },
            'rationale': [
                {
                    'text': 'This is rationale text',
                    'order': 1,
                },
            ],
            'reviewed': False,
            'active': True,
            'date_modified': '2018-01-01T12:01:00.000000Z',
            'date_reviewed': '2018-02-01T12:01:00.000000Z',
            'decks': [deck.deck_uuid],
            'references': ['This is reference text'],
            'tags': ['cardiology']
        }

    def test_accepts_valid_data(self):
        serializer = NewCardSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = NewCardSerializer(self.data)

        self.assertCountEqual(
            serializer.data.keys(),
            [
                'uuid', 'question', 'answer', 'rationale', 'reviewed', 'active',
                'date_modified', 'date_reviewed', 'decks', 'references', 'tags'
            ]
        )

    def test_card_uuid_cannot_be_set(self):
        invalid_data = self.data
        invalid_data['uuid'] = '1a'

        serializer = NewCardSerializer(data=invalid_data)

        # Check that serializer is valid
        self.assertTrue(serializer.is_valid())

    def test_invalid_date_handling(self):
        invalid_data = self.data
        invalid_data['date_reviewed'] = '2017-01-01'

        serializer = NewCardSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the date_reviewed error is present
        self.assertCountEqual(
            serializer.errors,
            ['date_reviewed']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['date_reviewed'],
            [
                'Datetime has wrong format. Use one of these formats instead: '
                'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'
            ]
        )

    def test_references_max_length(self):
        invalid_data = self.data
        invalid_data['references'] = ['a' * 501]

        serializer = NewCardSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the references error is present
        self.assertCountEqual(
            serializer.errors,
            ['references']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['references'],
            ['Ensure this field has no more than 500 characters.']
        )

    def test_references_list_min_length(self):
        invalid_data = self.data
        invalid_data['references'] = []

        serializer = NewCardSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the references error is present
        self.assertCountEqual(
            serializer.errors,
            ['references']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['references'],
            ['Ensure this field has at least 1 elements.']
        )

    def test_tags_max_length(self):
        invalid_data = self.data
        invalid_data['tags'] = ['a' * 101]

        serializer = NewCardSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the tags error is present
        self.assertCountEqual(
            serializer.errors,
            ['tags']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['tags'],
            ['Ensure this field has no more than 100 characters.']
        )

    def test_deck_uuid_validation(self):
        invalid_data = self.data
        invalid_data['decks'] = ['a']

        serializer = NewCardSerializer(data=self.data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the question error is present
        self.assertCountEqual(
            serializer.errors,
            ['decks']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['decks'],
            ['"a" is not a valid UUID.']
        )

    def test_custom_question_validation(self):
        invalid_data = self.data
        invalid_data['question'] = []

        serializer = NewCardSerializer(data=self.data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the question error is present
        self.assertCountEqual(
            serializer.errors,
            ['question']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['question'],
            ['A question is required.']
        )

    def test_custom_deck_validation(self):
        invalid_data = self.data
        invalid_data['decks'] = ['1e59d275-704f-479e-a911-ba2119f13d0d']

        serializer = NewCardSerializer(data=self.data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the question error is present
        self.assertCountEqual(
            serializer.errors,
            ['decks']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['decks'],
            ['Specified deck does not exist.']
        )
    def test_models_are_created(self):
        # Get initial counts
        card_count = Card.objects.count()
        card_deck_count = CardDeck.objects.count()
        reference_count = Reference.objects.count()

        # Create serializer and save data
        serializer = NewCardSerializer(data=self.data)
        serializer.is_valid()
        serializer.save()

        # Check for new card
        self.assertEqual(
            Card.objects.count(),
            card_count + 1
        )

        self.assertEqual(
            str(Card.objects.last()),
            'PartContainer (freeform)'
        )

        # Check for new card-deck match
        self.assertEqual(
            CardDeck.objects.count(),
            card_deck_count + 1
        )

        # Check for new reference match
        self.assertEqual(
            Reference.objects.count(),
            reference_count + 1
        )

        self.assertEqual(
            str(Reference.objects.last()),
            'This is reference text'
        )

    def test_tag_and_synonym_matching(self):
        # Create an existing tag and synonym
        tag = Tag.objects.create(
            tag_name='cardiology',
        )
        Synonym.objects.create(
            synonym_name='cardiology',
            tag=tag,
        )

        data = self.data
        data['tags'] = [tag.tag_name]

        # Get initial counts
        tag_count = Tag.objects.count()
        synonym_count = Synonym.objects.count()
        card_tag_count = CardTag.objects.count()

        # Create serializer and save data
        serializer = NewCardSerializer(data=self.data)
        serializer.is_valid()
        serializer.save()

        # Check that no new tags or synonyms were made
        self.assertEqual(Tag.objects.count(), tag_count)
        self.assertEqual(Synonym.objects.count(), synonym_count)

        # Check that a new card-tag match was made
        self.assertEqual(CardTag.objects.count(), card_tag_count + 1)

    def test_tag_and_synonym_creation(self):
        # Get initial counts
        tag_count = Tag.objects.count()
        synonym_count = Synonym.objects.count()
        card_tag_count = CardTag.objects.count()

        # Create serializer and save data
        serializer = NewCardSerializer(data=self.data)
        serializer.is_valid()
        serializer.save()

        # Check that a new tag was made
        self.assertEqual(Tag.objects.count(), tag_count + 1)
        self.assertEqual(str(Tag.objects.last()), 'cardiology')

        # Check that a new synonym was made
        self.assertEqual(Synonym.objects.count(), synonym_count + 1)
        self.assertEqual(str(Synonym.objects.last()), 'cardiology (synonym for cardiology)')

        # Check that a new card-tag match was made
        self.assertEqual(CardTag.objects.count(), card_tag_count + 1)
