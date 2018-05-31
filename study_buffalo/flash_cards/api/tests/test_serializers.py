from uuid import uuid4

from django.test import TestCase

from flash_cards import models
from flash_cards.api import serializers
from flash_cards.tests.utils import create_user


class SynonymSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            'synonym_name': 'cardio',
        }

    def test_accepts_valid_data(self):
        serializer = serializers.SynonymSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = serializers.SynonymSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

        self.assertCountEqual(
            serializer.validated_data.keys(),
            ['synonym_name', ]
        )

    def test_tag_name_max_length(self):
        invalid_text_data = self.data
        invalid_text_data['synonym_name'] = 'a' * 101

        serializer = serializers.SynonymSerializer(data=invalid_text_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the text error is present
        self.assertCountEqual(
            serializer.errors,
            ['synonym_name']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['synonym_name'],
            ['Ensure this field has no more than 100 characters.']
        )

class TagSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            'tag_name': 'cardiology',
            'synonyms': [],
        }

    def test_accepts_valid_data(self):
        serializer = serializers.TagSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = serializers.TagSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

        self.assertCountEqual(
            serializer.validated_data.keys(),
            ['tag_name', 'synonyms', ]
        )

    def test_tag_name_max_length(self):
        invalid_text_data = self.data
        invalid_text_data['tag_name'] = 'a' * 101

        serializer = serializers.TagSerializer(data=invalid_text_data)

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
            'deck_name': 'Cardiology',
            'reviewed': False,
            'active': True,
            'date_modified': '2018-01-01T12:01:00.000000Z',
            'date_reviewed': '2018-02-01T12:01:00.000000Z',
        }

    def test_accepts_valid_data(self):
        serializer = serializers.DeckSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = serializers.DeckSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

        self.assertCountEqual(
            serializer.validated_data.keys(),
            ['deck_name', 'reviewed', 'active', 'date_modified', 'date_reviewed']
        )

    def test_deck_name_max_length(self):
        invalid_data = self.data
        invalid_data['deck_name'] = 'a' * 256

        serializer = serializers.DeckSerializer(data=invalid_data)

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

        serializer = serializers.DeckSerializer(data=invalid_data)

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

class QuestionPartSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            'order': 1,
            'media_type': 't',
            'text': 'This is test text',
            'media': None,
        }

    def test_accepts_valid_data(self):
        serializer = serializers.QuestionPartSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = serializers.QuestionPartSerializer(self.data)

        self.assertCountEqual(
            serializer.data.keys(),
            ['order', 'media_type', 'text', 'media', ]
        )

    def test_media_type_choice_restriction(self):
        invalid_data = self.data
        invalid_data['media_type'] = 'aa'

        serializer = serializers.QuestionPartSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the deck_name error is present
        self.assertCountEqual(
            serializer.errors,
            ['media_type']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['media_type'],
            ['"aa" is not a valid choice.']
        )

    def test_text_max_length(self):
        invalid_data = self.data
        invalid_data['text'] = 'a' * 2001

        serializer = serializers.QuestionPartSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the deck_name error is present
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
        invalid_data = self.data
        invalid_data['order'] = 0

        serializer = serializers.QuestionPartSerializer(
            data=invalid_data,
        )

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the deck_name error is present
        self.assertCountEqual(
            serializer.errors,
            ['order']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['order'],
            ['Ensure this value is greater than or equal to 1.']
        )

class MultipleChoiceAnswerPartSerializerTest(TestCase):
    def setUp(self):
        answer = models.MultipleChoiceAnswer.objects.create(
            card=models.Card.objects.create(),
            order=1,
            correct=True,
        )

        self.data = {
            'multiple_choice_answer': answer.id,
            'order': 1,
            'media_type': 't',
            'text': 'This is a multiple choice answer',
            'media': None,
        }

    def test_accepts_valid_data(self):
        serializer = serializers.MultipleChoiceAnswerPartSerializer(
            data=self.data,
        )

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = serializers.MultipleChoiceAnswerPartSerializer(
            data=self.data,
        )

        self.assertTrue(serializer.is_valid())

        self.assertCountEqual(
            serializer.validated_data.keys(),
            ['multiple_choice_answer', 'order', 'media_type', 'text', 'media', ]
        )

    def test_text_max_length(self):
        invalid_data = self.data
        invalid_data['text'] = 'a' * 2001

        serializer = serializers.MultipleChoiceAnswerPartSerializer(
            data=invalid_data,
        )

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the deck_name error is present
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
        invalid_data = self.data
        invalid_data['order'] = 0

        serializer = serializers.MultipleChoiceAnswerPartSerializer(
            data=invalid_data,
        )

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the deck_name error is present
        self.assertCountEqual(
            serializer.errors,
            ['order']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['order'],
            ['Ensure this value is greater than or equal to 1.']
        )

class MultipleChoiceAnswerSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            'order': 1,
            'correct': True,
            'multiple_choice_answer_parts': [],
        }

    def test_accepts_valid_data(self):
        serializer = serializers.MultipleChoiceAnswerSerializer(
            data=self.data,
        )

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = serializers.MultipleChoiceAnswerSerializer(
            data=self.data,
        )

        self.assertTrue(serializer.is_valid())

        self.assertCountEqual(
            serializer.validated_data.keys(),
            ['order', 'correct', 'multiple_choice_answer_parts', ]
        )

    def test_order_min_value(self):
        invalid_data = self.data
        invalid_data['order'] = 0

        serializer = serializers.MultipleChoiceAnswerSerializer(
            data=invalid_data,
        )

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the deck_name error is present
        self.assertCountEqual(
            serializer.errors,
            ['order']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['order'],
            ['Ensure this value is greater than or equal to 1.']
        )

class MatchingAnswerPartSerializerTest(TestCase):
    def setUp(self):
        answer = models.MatchingAnswer.objects.create(
            card=models.Card.objects.create(),
            side='l',
            order=1,
            pair=None,
        )

        self.data = {
            'matching_answer': answer.id,
            'order': 1,
            'media_type': 't',
            'text': 'This is a matching answer',
            'media': None,
        }

    def test_accepts_valid_data(self):
        serializer = serializers.MatchingAnswerPartSerializer(
            data=self.data,
        )

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = serializers.MatchingAnswerPartSerializer(
            data=self.data,
        )

        self.assertTrue(serializer.is_valid())

        self.assertCountEqual(
            serializer.validated_data.keys(),
            ['matching_answer', 'order', 'media_type', 'text', 'media', ]
        )

    def test_text_max_length(self):
        invalid_data = self.data
        invalid_data['text'] = 'a' * 2001

        serializer = serializers.MatchingAnswerPartSerializer(
            data=invalid_data,
        )

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the deck_name error is present
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
        invalid_data = self.data
        invalid_data['order'] = 0

        serializer = serializers.MatchingAnswerPartSerializer(
            data=invalid_data,
        )

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the deck_name error is present
        self.assertCountEqual(
            serializer.errors,
            ['order']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['order'],
            ['Ensure this value is greater than or equal to 1.']
        )

class MatchingAnswerSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            'side': 'l',
            'order': 1,
            'pair': None,
            'matching_answer_parts': [],
        }

    def test_accepts_valid_data(self):
        serializer = serializers.MatchingAnswerSerializer(
            data=self.data,
        )

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = serializers.MatchingAnswerSerializer(
            data=self.data,
        )

        self.assertTrue(serializer.is_valid())

        self.assertCountEqual(
            serializer.validated_data.keys(),
            ['side', 'order', 'pair', 'matching_answer_parts', ]
        )

    def test_order_min_value(self):
        invalid_data = self.data
        invalid_data['order'] = 0

        serializer = serializers.MatchingAnswerSerializer(
            data=invalid_data,
        )

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the deck_name error is present
        self.assertCountEqual(
            serializer.errors,
            ['order']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['order'],
            ['Ensure this value is greater than or equal to 1.']
        )

class RationalePartSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            'order': 1,
            'media_type': 't',
            'text': 'This is rationale text',
            'media': None,
        }

    def test_accepts_valid_data(self):
        serializer = serializers.RationalePartSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = serializers.RationalePartSerializer(self.data)

        self.assertCountEqual(
            serializer.data.keys(),
            ['order', 'media_type', 'text', 'media', ]
        )

    def test_media_type_choice_restriction(self):
        invalid_data = self.data
        invalid_data['media_type'] = 'aa'

        serializer = serializers.RationalePartSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the deck_name error is present
        self.assertCountEqual(
            serializer.errors,
            ['media_type']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['media_type'],
            ['"aa" is not a valid choice.']
        )

    def test_text_max_length(self):
        invalid_data = self.data
        invalid_data['text'] = 'a' * 2001

        serializer = serializers.RationalePartSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the deck_name error is present
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
        invalid_data = self.data
        invalid_data['order'] = 0

        serializer = serializers.RationalePartSerializer(
            data=invalid_data,
        )

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the deck_name error is present
        self.assertCountEqual(
            serializer.errors,
            ['order']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['order'],
            ['Ensure this value is greater than or equal to 1.']
        )

class ReferenceSerializerTest(TestCase):
    def setUp(self):
        card = models.Card.objects.create()
        self.data = {
            'card': card.id,
            'reference': 'This is reference text',
        }

    def test_accepts_valid_data(self):
        serializer = serializers.ReferenceSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

    def test_expected_fields(self):
        serializer = serializers.ReferenceSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

        self.assertCountEqual(
            serializer.validated_data.keys(),
            ['card', 'reference', ]
        )

    def test_reference_max_length(self):
        invalid_text_data = self.data
        invalid_text_data['reference'] = 'a' * 501

        serializer = serializers.ReferenceSerializer(data=invalid_text_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the text error is present
        self.assertCountEqual(
            serializer.errors,
            ['reference']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['reference'],
            ['Ensure this field has no more than 500 characters.']
        )

class DeckForCardSerializer(TestCase):
    def setUp(self):
        deck = models.Deck.objects.create(deck_name='Cardiology')

        self.data = {
            'id': deck.id,
        }
        self.user = create_user()

    def test_accepts_valid_data(self):
        serializer = serializers.DeckForCardSerializer(data=self.data)

        self.assertTrue(serializer.is_valid())

    def test_id_validation(self):
        uuid = uuid4()

        serializer = serializers.DeckForCardSerializer(data={'id': uuid})

        self.assertFalse(serializer.is_valid())

        # Check that only the text error is present
        self.assertCountEqual(
            serializer.errors,
            ['id']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['id'],
            ['Provided deck does not exist: {}'.format(uuid)]
        )

# class NewCardSerializerTest(TestCase):
#     def setUp(self):
#         deck = Deck.objects.create(deck_name='cardiology')

#         self.data = {
#             'uuid': '',
#             'question': [
#                 {
#                     'text': 'This is question text part 1',
#                     'order': 1,
#                 },
#                 {
#                     'text': 'This is question text part 2',
#                     'order': 2,
#                 },
#             ],
#             'answer': {
#                 'freeform': [
#                     {
#                         'text': 'This is answer text',
#                         'order': 1,
#                     },
#                 ]
#             },
#             'rationale': [
#                 {
#                     'text': 'This is rationale text',
#                     'order': 1,
#                 },
#             ],
#             'reviewed': False,
#             'active': True,
#             'date_modified': '2018-01-01T12:01:00.000000Z',
#             'date_reviewed': '2018-02-01T12:01:00.000000Z',
#             'decks': [deck.deck_uuid],
#             'references': ['This is reference text'],
#             'tags': ['cardiology']
#         }

#     def test_accepts_valid_data(self):
#         serializer = NewCardSerializer(data=self.data)

#         self.assertTrue(serializer.is_valid())

#     def test_expected_fields(self):
#         serializer = NewCardSerializer(self.data)

#         self.assertCountEqual(
#             serializer.data.keys(),
#             [
#                 'uuid', 'question', 'answer', 'rationale', 'reviewed', 'active',
#                 'date_modified', 'date_reviewed', 'decks', 'references', 'tags'
#             ]
#         )

#     def test_card_uuid_cannot_be_set(self):
#         invalid_data = self.data
#         invalid_data['uuid'] = '1a'

#         serializer = NewCardSerializer(data=invalid_data)

#         # Check that serializer is valid
#         self.assertTrue(serializer.is_valid())

#     def test_invalid_date_handling(self):
#         invalid_data = self.data
#         invalid_data['date_reviewed'] = '2017-01-01'

#         serializer = NewCardSerializer(data=invalid_data)

#         # Check that serializer is invalid
#         self.assertFalse(serializer.is_valid())

#         # Check that only the date_reviewed error is present
#         self.assertCountEqual(
#             serializer.errors,
#             ['date_reviewed']
#         )

#         # Check that proper error message generated
#         self.assertEqual(
#             serializer.errors['date_reviewed'],
#             [
#                 'Datetime has wrong format. Use one of these formats instead: '
#                 'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'
#             ]
#         )

#     def test_references_max_length(self):
#         invalid_data = self.data
#         invalid_data['references'] = ['a' * 501]

#         serializer = NewCardSerializer(data=invalid_data)

#         # Check that serializer is invalid
#         self.assertFalse(serializer.is_valid())

#         # Check that only the references error is present
#         self.assertCountEqual(
#             serializer.errors,
#             ['references']
#         )

#         # Check that proper error message generated
#         self.assertEqual(
#             serializer.errors['references'],
#             ['Ensure this field has no more than 500 characters.']
#         )

#     def test_references_list_min_length(self):
#         invalid_data = self.data
#         invalid_data['references'] = []

#         serializer = NewCardSerializer(data=invalid_data)

#         # Check that serializer is invalid
#         self.assertFalse(serializer.is_valid())

#         # Check that only the references error is present
#         self.assertCountEqual(
#             serializer.errors,
#             ['references']
#         )

#         # Check that proper error message generated
#         self.assertEqual(
#             serializer.errors['references'],
#             ['Ensure this field has at least 1 elements.']
#         )

#     def test_tags_max_length(self):
#         invalid_data = self.data
#         invalid_data['tags'] = ['a' * 101]

#         serializer = NewCardSerializer(data=invalid_data)

#         # Check that serializer is invalid
#         self.assertFalse(serializer.is_valid())

#         # Check that only the tags error is present
#         self.assertCountEqual(
#             serializer.errors,
#             ['tags']
#         )

#         # Check that proper error message generated
#         self.assertEqual(
#             serializer.errors['tags'],
#             ['Ensure this field has no more than 100 characters.']
#         )

#     def test_deck_uuid_validation(self):
#         invalid_data = self.data
#         invalid_data['decks'] = ['a']

#         serializer = NewCardSerializer(data=self.data)

#         # Check that serializer is invalid
#         self.assertFalse(serializer.is_valid())

#         # Check that only the question error is present
#         self.assertCountEqual(
#             serializer.errors,
#             ['decks']
#         )

#         # Check that proper error message generated
#         self.assertEqual(
#             serializer.errors['decks'],
#             ['"a" is not a valid UUID.']
#         )

#     def test_custom_question_validation(self):
#         invalid_data = self.data
#         invalid_data['question'] = []

#         serializer = NewCardSerializer(data=self.data)

#         # Check that serializer is invalid
#         self.assertFalse(serializer.is_valid())

#         # Check that only the question error is present
#         self.assertCountEqual(
#             serializer.errors,
#             ['question']
#         )

#         # Check that proper error message generated
#         self.assertEqual(
#             serializer.errors['question'],
#             ['A question is required.']
#         )

#     def test_custom_deck_validation(self):
#         invalid_data = self.data
#         invalid_data['decks'] = ['1e59d275-704f-479e-a911-ba2119f13d0d']

#         serializer = NewCardSerializer(data=self.data)

#         # Check that serializer is invalid
#         self.assertFalse(serializer.is_valid())

#         # Check that only the question error is present
#         self.assertCountEqual(
#             serializer.errors,
#             ['decks']
#         )

#         # Check that proper error message generated
#         self.assertEqual(
#             serializer.errors['decks'],
#             ['Specified deck does not exist.']
#         )
#     def test_models_are_created(self):
#         # Get initial counts
#         card_count = Card.objects.count()
#         card_deck_count = CardDeck.objects.count()
#         reference_count = Reference.objects.count()

#         # Create serializer and save data
#         serializer = NewCardSerializer(data=self.data)
#         serializer.is_valid()
#         serializer.save()

#         # Check for new card
#         self.assertEqual(
#             Card.objects.count(),
#             card_count + 1
#         )

#         self.assertEqual(
#             str(Card.objects.last()),
#             'This is question text part 1 This is ... (freeform)'
#         )

#         # Check for new card-deck match
#         self.assertEqual(
#             CardDeck.objects.count(),
#             card_deck_count + 1
#         )

#         # Check for new reference match
#         self.assertEqual(
#             Reference.objects.count(),
#             reference_count + 1
#         )

#         self.assertEqual(
#             str(Reference.objects.last()),
#             'This is reference text'
#         )

#     def test_tag_and_synonym_matching(self):
#         # Create an existing tag and synonym
#         tag = Tag.objects.create(
#             tag_name='cardiology',
#         )
#         Synonym.objects.create(
#             synonym_name='cardiology',
#             tag=tag,
#         )

#         data = self.data
#         data['tags'] = [tag.tag_name]

#         # Get initial counts
#         tag_count = Tag.objects.count()
#         synonym_count = Synonym.objects.count()
#         card_tag_count = CardTag.objects.count()

#         # Create serializer and save data
#         serializer = NewCardSerializer(data=self.data)
#         serializer.is_valid()
#         serializer.save()

#         # Check that no new tags or synonyms were made
#         self.assertEqual(Tag.objects.count(), tag_count)
#         self.assertEqual(Synonym.objects.count(), synonym_count)

#         # Check that a new card-tag match was made
#         self.assertEqual(CardTag.objects.count(), card_tag_count + 1)

#     def test_tag_and_synonym_creation(self):
#         # Get initial counts
#         tag_count = Tag.objects.count()
#         synonym_count = Synonym.objects.count()
#         card_tag_count = CardTag.objects.count()

#         # Create serializer and save data
#         serializer = NewCardSerializer(data=self.data)
#         serializer.is_valid()
#         serializer.save()

#         # Check that a new tag was made
#         self.assertEqual(Tag.objects.count(), tag_count + 1)
#         self.assertEqual(str(Tag.objects.last()), 'cardiology')

#         # Check that a new synonym was made
#         self.assertEqual(Synonym.objects.count(), synonym_count + 1)
#         self.assertEqual(str(Synonym.objects.last()), 'cardiology (synonym for cardiology)')

#         # Check that a new card-tag match was made
#         self.assertEqual(CardTag.objects.count(), card_tag_count + 1)
