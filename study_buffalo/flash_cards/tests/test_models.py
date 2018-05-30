from django.test import TestCase

from flash_cards.models import TextPart

from .utils import (
    create_text_part, create_multiple_choice_answers, create_matching_answers,
    #create_multiple_choice_card, create_matching_card,
    create_freeform_card, create_deck, create_reference, create_tag, create_synonym,
    create_deck_stats, create_user_stats, create_card_feedback, create_deck_feedback
)

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

        # Test correct label
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
            '1) Answer 1 (incorrect)'
        )

        # Test an correct response
        self.assertEqual(
            str(self.answers[1]),
            '2) Answer 2 (correct)'
        )

class MatchingAnswerModelTest(TestCase):
    '''Test functions for the MatchingAnswer model'''
    def setUp(self):
        answer_container = create_matching_answers()
        self.answers = answer_container.matchinganswer_set.all()

    def test_labels(self):
        # Test side label
        self.assertEqual(
            self.answers[0]._meta.get_field('side').verbose_name,
            'side',
        )

        # Test order label
        self.assertEqual(
            self.answers[0]._meta.get_field('order').verbose_name,
            'order',
        )

        # Test pair label
        self.assertEqual(
            self.answers[0]._meta.get_field('pair').verbose_name,
            'pair',
        )

        # Test question_container label
        self.assertEqual(
            self.answers[0]._meta.get_field('question_container').verbose_name,
            'question container',
        )

        # Test part container label
        self.assertEqual(
            self.answers[0]._meta.get_field('part_container').verbose_name,
            'part container',
        )

    def test_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        self.assertEqual(
            str(self.answers[0]),
            '1) Left: Answer 1 (left)'
        )

# class CardModelMultipleChoiceTest(TestCase):
#     def setUp(self):
#         self.card = create_multiple_choice_card()

# class CardModelMatchingTest(TestCase):
#     def setUp(self):
#         self.card = create_matching_card()

class CardModelFreeformTest(TestCase):
    def setUp(self):
        self.card = create_freeform_card()

    def test_labels(self):
        # Test card_uuid label
        self.assertEqual(
            self.card._meta.get_field('card_uuid').verbose_name,
            'card UUID',
        )

        # Test question label
        self.assertEqual(
            self.card._meta.get_field('question').verbose_name,
            'question',
        )

        # Test answer_multiple_choice label
        self.assertEqual(
            self.card._meta.get_field('answer_multiple_choice').verbose_name,
            'multiple choice answer',
        )

        # Test answer_matching label
        self.assertEqual(
            self.card._meta.get_field('answer_matching').verbose_name,
            'matching answer',
        )

        # Test answer_freeform label
        self.assertEqual(
            self.card._meta.get_field('answer_freeform').verbose_name,
            'freeform answer',
        )

        # Test rationale label
        self.assertEqual(
            self.card._meta.get_field('rationale').verbose_name,
            'answer rationale',
        )

        # Test reviewed label
        self.assertEqual(
            self.card._meta.get_field('reviewed').verbose_name,
            'reviewed',
        )

        # Test active label
        self.assertEqual(
            self.card._meta.get_field('active').verbose_name,
            'active',
        )

        # Test date_modified label
        self.assertEqual(
            self.card._meta.get_field('date_modified').verbose_name,
            'date modified',
        )

        # Test date_reviewed label
        self.assertEqual(
            self.card._meta.get_field('date_reviewed').verbose_name,
            'date reviewed',
        )

    def test_short_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        self.assertEqual(
            str(self.card),
            'This is a question (freeform)'
        )

    def test_long_string_representation(self):
        long_card = self.card

        long_card_text = long_card.question.textpart_set.first()
        long_card_text.text = 'a' * 50
        long_card_text.save()

        self.assertEqual(
            str(long_card),
            'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa... (freeform)'
        )

class DeckModelTest(TestCase):
    def setUp(self):
        self.deck = create_deck('Cardiology Questions')

    def test_labels(self):
        # Test deck_uuid label
        self.assertEqual(
            self.deck._meta.get_field('deck_uuid').verbose_name,
            'deck UUID',
        )

        # Test deck_name label
        self.assertEqual(
            self.deck._meta.get_field('deck_name').verbose_name,
            'deck name',
        )

        # Test reviewed label
        self.assertEqual(
            self.deck._meta.get_field('reviewed').verbose_name,
            'reviewed',
        )

        # Test active label
        self.assertEqual(
            self.deck._meta.get_field('active').verbose_name,
            'active',
        )

        # Test date_modified label
        self.assertEqual(
            self.deck._meta.get_field('date_modified').verbose_name,
            'date modified',
        )

        # Test date_reviewed label
        self.assertEqual(
            self.deck._meta.get_field('date_reviewed').verbose_name,
            'date reviewed',
        )

    def test_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        self.assertEqual(
            str(self.deck),
            'Cardiology Questions'
        )

class ReferenceModelTest(TestCase):
    def setUp(self):
        self.reference = create_reference()

    def test_labels(self):
        # Test card label
        self.assertEqual(
            self.reference._meta.get_field('card').verbose_name,
            'card',
        )

        # Test reference label
        self.assertEqual(
            self.reference._meta.get_field('reference').verbose_name,
            'reference',
        )

    def test_reference_max_length(self):
        self.assertEqual(
            self.reference._meta.get_field('reference').max_length,
            500
        )

    def test_short_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        self.assertEqual(
            str(self.reference),
            'This is a reference'
        )

    def test_long_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        long_reference = self.reference
        long_reference.reference = 'a' * 51
        long_reference.save()

        self.assertEqual(
            str(self.reference),
            'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa...'
        )

class TagModelTest(TestCase):
    def setUp(self):
        self.tag = create_tag()

    def test_labels(self):
        # Test tag_name label
        self.assertEqual(
            self.tag._meta.get_field('tag_name').verbose_name,
            'tag name',
        )

    def test_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        self.assertEqual(
            str(self.tag),
            'cardiology'
        )

class SynonymModelTest(TestCase):
    def setUp(self):
        self.synonym = create_synonym()

    def test_labels(self):
        # Test tag label
        self.assertEqual(
            self.synonym._meta.get_field('tag').verbose_name,
            'tag',
        )

        # Test synonym_name label
        self.assertEqual(
            self.synonym._meta.get_field('synonym_name').verbose_name,
            'synonym name',
        )

    def test_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        self.assertEqual(
            str(self.synonym),
            'cardio (synonym for cardiology)'
        )

class DeckStatsModelTest(TestCase):
    def setUp(self):
        self.deck_stats = create_deck_stats()


    def test_labels(self):
        # Test user label
        self.assertEqual(
            self.deck_stats._meta.get_field('user').verbose_name,
            'user',
        )

        # Test deck label
        self.assertEqual(
            self.deck_stats._meta.get_field('deck').verbose_name,
            'deck',
        )

        # Test date_completed label
        self.assertEqual(
            self.deck_stats._meta.get_field('date_completed').verbose_name,
            'date completed',
        )

        # Test number_questions label
        self.assertEqual(
            self.deck_stats._meta.get_field('number_questions').verbose_name,
            'number of questions',
        )

        # Test number_correct label
        self.assertEqual(
            self.deck_stats._meta.get_field('number_correct').verbose_name,
            'number correct',
        )

        # Test number_partially_correct label
        self.assertEqual(
            self.deck_stats._meta.get_field('number_partially_correct').verbose_name,
            'number partially correct',
        )

        # Test number_incorrect label
        self.assertEqual(
            self.deck_stats._meta.get_field('number_incorrect').verbose_name,
            'number incorrect',
        )

    def test_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        self.assertEqual(
            str(self.deck_stats),
            'Cardiology stats for Regular User'
        )

class UserStatsModelTest(TestCase):
    def setUp(self):
        self.user_stats = create_user_stats()

    def test_labels(self):
        # Test user label
        self.assertEqual(
            self.user_stats._meta.get_field('user').verbose_name,
            'user',
        )

        # Test number_decks label
        self.assertEqual(
            self.user_stats._meta.get_field('number_decks').verbose_name,
            'decks completed',
        )

        # Test number_questions label
        self.assertEqual(
            self.user_stats._meta.get_field('number_questions').verbose_name,
            'questions completed',
        )

        # Test number_correct label
        self.assertEqual(
            self.user_stats._meta.get_field('number_correct').verbose_name,
            'number correct',
        )

        # Test number_partially_correct label
        self.assertEqual(
            self.user_stats._meta.get_field('number_partially_correct').verbose_name,
            'number partially correct',
        )

        # Test number_incorrect label
        self.assertEqual(
            self.user_stats._meta.get_field('number_incorrect').verbose_name,
            'number incorrect',
        )

    def test_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        self.assertEqual(
            str(self.user_stats),
            'Stats for Regular User'
        )

class CardFeedbackModelTest(TestCase):
    def setUp(self):
        self.feedback = create_card_feedback()

    def test_labels(self):
        # Test user label
        self.assertEqual(
            self.feedback._meta.get_field('user').verbose_name,
            'user',
        )

        # Test date_submitted label
        self.assertEqual(
            self.feedback._meta.get_field('date_submitted').verbose_name,
            'date submitted',
        )

        # Test comment label
        self.assertEqual(
            self.feedback._meta.get_field('comment').verbose_name,
            'comment',
        )

        # Test card label
        self.assertEqual(
            self.feedback._meta.get_field('card').verbose_name,
            'card',
        )

    def test_comment_max_length(self):
        self.assertEqual(
            self.feedback._meta.get_field('comment').max_length,
            2000
        )

    def test_short_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        self.assertEqual(
            str(self.feedback),
            'This is a question (freeform) feedback: This is a feedback comment'
        )

    def test_long_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        long_feedback = self.feedback
        long_feedback.comment = 'a' * 51
        long_feedback.save()

        self.assertEqual(
            str(long_feedback),
            'This is a question (freeform) feedback: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa...'
        )
class DeckFeedbackModelTest(TestCase):
    def setUp(self):
        self.feedback = create_deck_feedback()

    def test_labels(self):
        # Test user label
        self.assertEqual(
            self.feedback._meta.get_field('user').verbose_name,
            'user',
        )

        # Test date_submitted label
        self.assertEqual(
            self.feedback._meta.get_field('date_submitted').verbose_name,
            'date submitted',
        )

        # Test comment label
        self.assertEqual(
            self.feedback._meta.get_field('comment').verbose_name,
            'comment',
        )

        # Test deck label
        self.assertEqual(
            self.feedback._meta.get_field('deck').verbose_name,
            'deck',
        )

    def test_comment_max_length(self):
        self.assertEqual(
            self.feedback._meta.get_field('comment').max_length,
            2000
        )

    def test_short_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        self.assertEqual(
            str(self.feedback),
            'Cardiology feedback: This is a feedback comment'
        )

    def test_long_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        long_feedback = self.feedback
        long_feedback.comment = 'a' * 51
        long_feedback.save()

        self.assertEqual(
            str(long_feedback),
            'Cardiology feedback: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa...'
        )
