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
