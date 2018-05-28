from django.test import TestCase

from flash_cards.models import TextPart

from .utils import create_text_part, create_multiple_choice_answers

class TextPartModelTest(TestCase):
    '''Test functions for the TextPart model'''
    def setUp(self):
        self.answers = create_text_part('This is test text.')

    def test_labels(self):
        text_part = TextPart.objects.first()

        # Test text label
        self.assertEqual(
            text_part._meta.get_field('text').verbose_name,
            'text',
        )

        # Test order label
        self.assertEqual(
            text_part._meta.get_field('order').verbose_name,
            'order',
        )

        # Test container label
        self.assertEqual(
            text_part._meta.get_field('container').verbose_name,
            'container',
        )

    def test_text_max_length(self):
        text_part = TextPart.objects.first()

        self.assertEqual(text_part._meta.get_field('text').max_length, 2000)

    def test_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        # Get the text part
        text_part = TextPart.objects.first()

        self.assertEqual(str(text_part), '1 - This is test text.')

# class MediaPartModelTest(TestCase):
#     '''Test functions for the MediaPart model'''
#     def setUp(self):
#         create_media_part()

#     def test_labels(self):
#         media_part = MediaPart.objects.first()

#         # Test text label
#         self.assertEqual(
#             text_part._meta.get_field('media_type').verbose_name,
#             'media_type',
#         )

#         # Test order label
#         self.assertEqual(
#             text_part._meta.get_field('order').verbose_name,
#             'order',
#         )

#         # Test container label
#         self.assertEqual(
#             text_part._meta.get_field('container').verbose_name,
#             'container',
#         )

#     def test_string_representation(self):
#         '''Tests that the model string representaton returns as expected'''
#         # Get the text part
#         text_part = TextPart.objects.first()

#         self.assertEqual(str(text_part), '1 - i - SOMETHING.')

class MultipleChoiceAnswerModelTest(TestCase):
    '''Test functions for the MultipleChoiceAnswer model'''
    def setUp(self):
        answer_container = create_multiple_choice_answers()
        self.answers = answer_container.multiplechoiceanswer_set.all()

    def test_labels(self):
        # Test text label
        self.assertEqual(
            self.answers[0]._meta.get_field('order').verbose_name,
            'order',
        )

        # Test order label
        self.assertEqual(
            self.answers[0]._meta.get_field('correct').verbose_name,
            'correct',
        )

        # Test container label
        self.assertEqual(
            self.answers[0]._meta.get_field('container').verbose_name,
            'container',
        )

        # Test part container label
        self.assertEqual(
            self.answers[0]._meta.get_field('part_container').verbose_name,
            'part container',
        )

    def test_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        # Test an incorrect response
        self.assertEqual(
            str(self.answers[0]),
            '1) PartContainer (incorrect)'
        )

        # Test an correct response
        self.assertEqual(
            str(self.answers[1]),
            '2) PartContainer (correct)'
        )

class MatchingAnswerModelTest(TestCase):
    '''Test functions for the MatchingAnswer model'''
    def setUp(self):
        answer_container = create_matching_answers()
        self.answers = answer_container.matchinganswer_set.all()

    def test_labels(self):
        # Test text label
        self.assertEqual(
            self.answers[0]._meta.get_field('order').verbose_name,
            'order',
        )

        # Test order label
        self.assertEqual(
            self.answers[0]._meta.get_field('correct').verbose_name,
            'correct',
        )

        # Test container label
        self.assertEqual(
            self.answers[0]._meta.get_field('container').verbose_name,
            'container',
        )

        # Test part container label
        self.assertEqual(
            self.answers[0]._meta.get_field('part_container').verbose_name,
            'part container',
        )

    def test_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        # Test an incorrect response
        self.assertEqual(
            str(self.answers[0]),
            '1) PartContainer (incorrect)'
        )

        # Test an correct response
        self.assertEqual(
            str(self.answers[1]),
            '2) PartContainer (correct)'
        )
