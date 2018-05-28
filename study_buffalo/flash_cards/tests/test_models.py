from django.test import TestCase

from flash_cards.models import TextPart

from .utils import create_text_part

class TextPartModelTest(TestCase):
    '''Test functions for the TextPart model'''
    def setUp(self):
        create_text_part()

    def test_labels(self):
        text_part = TextPart.objects.first()

        # Test text label
        self.assertEqual(
            text_part._meta.get_field("text").verbose_name,
            "text",
        )

        # Test order label
        self.assertEqual(
            text_part._meta.get_field("order").verbose_name,
            "order",
        )


        # Test container label
        self.assertEqual(
            text_part._meta.get_field("container").verbose_name,
            "container",
        )

    def test_text_max_length(self):
        text_part = TextPart.objects.first()

        self.assertEqual(
            text_part._meta.get_field("text").max_length,
            2000
        )
