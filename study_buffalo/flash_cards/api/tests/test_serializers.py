from uuid import uuid4

from django.test import TestCase

from flash_cards import models
from flash_cards.api import serializers


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
            'synonyms': [
                {'synonym_name': 'cardio'},
            ],
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

    def test_custom_create_with_synonym(self):
        # Count model numbers
        tag_total = models.Tag.objects.all().count()
        synonym_total = models.Synonym.objects.all().count()

        # Serialize and save data
        serializer = serializers.TagSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Check that models were created
        self.assertEqual(
            models.Tag.objects.all().count(),
            tag_total + 1
        )

        self.assertEqual(
            models.Synonym.objects.all().count(),
            synonym_total + 2
        )

    def test_custom_create_without_synonym(self):
        # Count model numbers
        tag_total = models.Tag.objects.all().count()
        synonym_total = models.Synonym.objects.all().count()

        # Serialize and save data
        serializer = serializers.TagSerializer(data={'tag_name': 'cardiology'})
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Check that models were created
        self.assertEqual(
            models.Tag.objects.all().count(),
            tag_total + 1
        )

        self.assertEqual(
            models.Synonym.objects.all().count(),
            synonym_total + 1
        )

    def test_custom_update_with_synonym(self):
        tag = models.Tag.objects.create(
            tag_name='cardio'
        )
        models.Synonym.objects.create(
            tag=tag,
            synonym_name='heart stuff'
        )

        # Count model numbers
        tag_total = models.Tag.objects.all().count()
        synonym_total = models.Synonym.objects.all().count()

        # Serialize and save data
        serializer = serializers.TagSerializer(tag, data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Check that models were updated/created
        self.assertEqual(
            models.Tag.objects.all().count(),
            tag_total
        )

        self.assertEqual(
            models.Synonym.objects.all().count(),
            synonym_total + 2
        )

    def test_custom_update_without_synonym(self):
        tag = models.Tag.objects.create(
            tag_name='cardio'
        )
        models.Synonym.objects.create(
            tag=tag,
            synonym_name='cardio'
        )

        # Count model numbers
        tag_total = models.Tag.objects.all().count()
        synonym_total = models.Synonym.objects.all().count()

        # Serialize and save data
        serializer = serializers.TagSerializer(tag, data={'tag_name': 'cardiology'})
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Check that models were updated/created
        self.assertEqual(
            models.Tag.objects.all().count(),
            tag_total
        )

        self.assertEqual(
            models.Synonym.objects.all().count(),
            synonym_total + 1
        )

class DeckSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            'deck_name': 'Cardiology',
            'description': 'A cardiology study deck',
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
            ['deck_name', 'description', 'reviewed', 'active', 'date_modified', 'date_reviewed']
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

    def test_description_name_max_length(self):
        invalid_data = self.data
        invalid_data['description'] = 'a' * 501

        serializer = serializers.DeckSerializer(data=invalid_data)

        # Check that serializer is invalid
        self.assertFalse(serializer.is_valid())

        # Check that only the deck_name error is present
        self.assertCountEqual(
            serializer.errors,
            ['description']
        )

        # Check that proper error message generated
        self.assertEqual(
            serializer.errors['description'],
            ['Ensure this field has no more than 500 characters.']
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
        self.data = {
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
            ['order', 'media_type', 'text', 'media', ]
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
        self.data = {
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
            ['order', 'media_type', 'text', 'media', ]
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
        self.data = {
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
            ['reference', ]
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
