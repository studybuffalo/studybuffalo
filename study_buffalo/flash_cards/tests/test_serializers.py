from django.test import TestCase

from flash_cards.serializers import (
    PartSerializer, MultipleChoiceSerializer, MatchingSerializer, AnswerSerializer,
    TagSerializer, DeckSerializer, CardSerializer, NewCardSerializer
)

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

    def test_text_field_content(self):
        serializer = PartSerializer(self.text_data)

        self.assertEqual(
            serializer.data['text'],
            'This is test text'
        )

    def test_order_field_content(self):
        serializer = PartSerializer(self.text_data)

        self.assertEqual(
            serializer.data['order'],
            1
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

    def test_order_field_content(self):
        serializer = MultipleChoiceSerializer(self.data)

        self.assertEqual(
            serializer.data['order'],
            1
        )

    def test_correct_field_content(self):
        serializer = MultipleChoiceSerializer(self.data)

        self.assertEqual(
            serializer.data['correct'],
            True
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

    def test_side_field_content(self):
        serializer = MatchingSerializer(self.data)

        self.assertEqual(
            serializer.data['side'],
            'l'
        )

    def test_order_field_content(self):
        serializer = MatchingSerializer(self.data)

        self.assertEqual(
            serializer.data['order'],
            1
        )

    def test_pair_field_content(self):
        serializer = MatchingSerializer(self.data)

        self.assertEqual(
            serializer.data['pair'],
            1
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

    def test_tag_name_field_content(self):
        serializer = TagSerializer(self.data)

        self.assertEqual(
            serializer.data['tag_name'],
            'cardiology'
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

    def test_deck_uuid_field_content(self):
        serializer = DeckSerializer(self.data)

        self.assertEqual(
            serializer.data['deck_uuid'],
            '1e59d275-704f-479e-a911-ba2119f13d0d'
        )

    def test_deck_name_field_content(self):
        serializer = DeckSerializer(self.data)

        self.assertEqual(
            serializer.data['deck_name'],
            'Cardiology'
        )

    def test_reviewed_field_content(self):
        serializer = DeckSerializer(self.data)

        self.assertEqual(
            serializer.data['reviewed'],
            False
        )

    def test_active_field_content(self):
        serializer = DeckSerializer(self.data)

        self.assertEqual(
            serializer.data['active'],
            True
        )

    def test_date_modified_content(self):
        serializer = DeckSerializer(self.data)

        self.assertEqual(
            serializer.data['date_modified'],
            True
        )
