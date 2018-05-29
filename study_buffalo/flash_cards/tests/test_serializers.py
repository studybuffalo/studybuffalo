from django.test import TestCase

from flash_cards.serializers import PartSerializer

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
