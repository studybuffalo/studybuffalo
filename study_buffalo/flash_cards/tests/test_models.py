from django.core.exceptions import ValidationError
from django.test import TestCase

from flash_cards import models
from flash_cards.tests import utils


class BaseAbstractModelTest(TestCase):
    def setUp(self):
        self.base_abstract = models.BaseAbstractModel()

    def test_labels(self):
        # Test id label
        self.assertEqual(
            self.base_abstract._meta.get_field('id').verbose_name,
            'id',
        )

class AbstractPartModelTest(TestCase):
    def setUp(self):
        self.part = models.AbstractPart(
            order=1,
            media_type='t',
            text='This is text',
            media=None
        )

    def test_labels(self):
        # Test order label
        self.assertEqual(
            self.part._meta.get_field('order').verbose_name,
            'order',
        )

        # Test media_type label
        self.assertEqual(
            self.part._meta.get_field('media_type').verbose_name,
            'media type',
        )

        # Test text label
        self.assertEqual(
            self.part._meta.get_field('text').verbose_name,
            'text',
        )

        # Test media label
        self.assertEqual(
            self.part._meta.get_field('media').verbose_name,
            'media',
        )

    def test_order_validation(self):
        part = models.AbstractPart(order=0, media_type='t')

        try:
            part.clean_fields()
            errors = False
        except ValidationError as e:
            errors = dict(e)

        # Check for errors
        self.assertTrue(errors)

        # Check for proper error
        self.assertTrue('order' in errors)
        self.assertEqual(
            errors['order'],
            ["Ensure this value is greater than or equal to 1."]
        )
    def test_media_type_max_length(self):
        self.assertEqual(self.part._meta.get_field('media_type').max_length, 1)

    def test_media_type_choices(self):
        part = models.AbstractPart(media_type='z')

        try:
            part.clean_fields()
            errors = False
        except ValidationError as e:
            errors = dict(e)

        # Check for errors
        self.assertTrue(errors)

        # Check for proper error
        self.assertTrue('media_type' in errors)
        self.assertEqual(
            errors['media_type'],
            ["Value 'z' is not a valid choice."]
        )

    def test_text_max_length(self):
        self.assertEqual(self.part._meta.get_field('text').max_length, 2000)

    def test_short_text_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        self.assertEqual(str(self.part), 'This is text')

    def test_long_text_string_representation(self):
        part = models.AbstractPart(text='a' * 41)

        self.assertEqual(str(part), 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa...')

    # TODO: Create tests for the other media types when working properly

class TagModelTest(TestCase):
    def setUp(self):
        self.tag = utils.create_tag()

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
        self.synonym = utils.create_synonym()

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

class DeckModelTest(TestCase):
    def setUp(self):
        self.deck = utils.create_deck('Cardiology Questions')

    def test_labels(self):
        # Test deck_uuid label
        self.assertEqual(
            self.deck._meta.get_field('id').verbose_name,
            'id',
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

class QuestionPartModelTest(TestCase):
    def setUp(self):
        self.part = utils.create_question_part(text='This is a question')

    def test_labels(self):
        # Test card label
        self.assertEqual(
            self.part._meta.get_field('card').verbose_name,
            'card',
        )

class MultipleChoiceAnswerModelTest(TestCase):
    def setUp(self):
        answer_part = utils.create_multiple_choice_answer_part(
            'This is a multiple choice answer'
        )
        self.answer = answer_part.multiple_choice_answer

    def test_labels(self):
        # Test id label
        self.assertEqual(
            self.answer._meta.get_field('id').verbose_name,
            'id',
        )

        # Test card label
        self.assertEqual(
            self.answer._meta.get_field('card').verbose_name,
            'card',
        )

        # Test order label
        self.assertEqual(
            self.answer._meta.get_field('order').verbose_name,
            'order',
        )

        # Test correct label
        self.assertEqual(
            self.answer._meta.get_field('correct').verbose_name,
            'correct',
        )

    def test_short_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        self.assertEqual(
            str(self.answer),
            '1) This is a multiple choice answer'
        )

    def test_long_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        # Create a long answer
        answer_part = utils.create_multiple_choice_answer_part(
            'This is a very very very very long multiple choice answer'
        )
        answer = answer_part.multiple_choice_answer

        self.assertEqual(
            str(answer),
            '1) This is a very very very very long...'
        )

class MultipleChoiceAnswerPartModelTest(TestCase):
    def setUp(self):
        self.part = utils.create_multiple_choice_answer_part(
            text='This is an MC answer'
        )

    def test_labels(self):
        # Test multiple_choice_answer label
        self.assertEqual(
            self.part._meta.get_field('multiple_choice_answer').verbose_name,
            'multiple choice answer',
        )

class MatchingAnswerModelTest(TestCase):
    def setUp(self):
        answer_part = utils.create_matching_answer_part(
            'This is a matching answer'
        )
        self.answer = answer_part.matching_answer

    def test_labels(self):
        # Test id label
        self.assertEqual(
            self.answer._meta.get_field('id').verbose_name,
            'id',
        )

        # Test card label
        self.assertEqual(
            self.answer._meta.get_field('card').verbose_name,
            'card',
        )

        # Test side label
        self.assertEqual(
            self.answer._meta.get_field('side').verbose_name,
            'side',
        )

        # Test order label
        self.assertEqual(
            self.answer._meta.get_field('order').verbose_name,
            'order',
        )

        # Test pair label
        self.assertEqual(
            self.answer._meta.get_field('pair').verbose_name,
            'pair',
        )

    def test_short_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        self.assertEqual(
            str(self.answer),
            'L1) This is a matching answer'
        )

    def test_long_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        # Create a long answer
        answer_part = utils.create_matching_answer_part(
            'This is a very very very very long matching answer'
        )
        answer = answer_part.matching_answer

        self.assertEqual(
            str(answer),
            'L1) This is a very very very very lon...'
        )

class MatchingAnswerPartModelTest(TestCase):
    def setUp(self):
        self.part = utils.create_matching_answer_part(
            text='This is a matching answer'
        )

    def test_labels(self):
        # Test matching_answer label
        self.assertEqual(
            self.part._meta.get_field('matching_answer').verbose_name,
            'matching answer',
        )

class FreeformAnswerPartModelTest(TestCase):
    def setUp(self):
        self.part = utils.create_freeform_answer_part(text='This is a freeform answer')

    def test_labels(self):
        # Test card label
        self.assertEqual(
            self.part._meta.get_field('card').verbose_name,
            'card',
        )

class RationalePartModelTest(TestCase):
    def setUp(self):
        self.part = utils.create_rationale_part(text='This is some rationale')

    def test_labels(self):
        # Test card label
        self.assertEqual(
            self.part._meta.get_field('card').verbose_name,
            'card',
        )

class ReferenceModelTest(TestCase):
    def setUp(self):
        self.reference = utils.create_reference()

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

class CardDeckModelTest(TestCase):
    def setUp(self):
        card = utils.create_card()
        deck = utils.create_deck('Cardiology')

        self.card_deck = utils.create_card_deck_match(card, deck)

    def test_labels(self):
        # Test card label
        self.assertEqual(
            self.card_deck._meta.get_field('card').verbose_name,
            'card',
        )

        # Test deck label
        self.assertEqual(
            self.card_deck._meta.get_field('deck').verbose_name,
            'deck',
        )

class CardTagModelTest(TestCase):
    def setUp(self):
        card = utils.create_card()
        tag = utils.create_tag()

        self.card_tag = utils.create_card_tag_match(card, tag)

    def test_labels(self):
        # Test card label
        self.assertEqual(
            self.card_tag._meta.get_field('card').verbose_name,
            'card',
        )

        # Test tag label
        self.assertEqual(
            self.card_tag._meta.get_field('tag').verbose_name,
            'tag',
        )

class DeckStatsModelTest(TestCase):
    def setUp(self):
        self.deck_stats = utils.create_deck_stats()


    def test_labels(self):
        # Test id label
        self.assertEqual(
            self.deck_stats._meta.get_field('id').verbose_name,
            'id',
        )

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
        self.user_stats = utils.create_user_stats()

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
        self.feedback = utils.create_card_feedback()

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
        # Update the question
        self.feedback.comment = 'a' * 51
        self.feedback.save()

        self.assertEqual(
            str(self.feedback),
            'This is a question (freeform) feedback: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa...'
        )

class DeckFeedbackModelTest(TestCase):
    def setUp(self):
        self.feedback = utils.create_deck_feedback()

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

class CardModelFreeformTest(TestCase):
    def setUp(self):
        self.card = utils.create_freeform_card()

    def test_labels(self):
        # Test id label
        self.assertEqual(
            self.card._meta.get_field('id').verbose_name,
            'id',
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

        # Test tags label
        self.assertEqual(
            self.card._meta.get_field('tags').verbose_name,
            'tags',
        )

        # Test decks label
        self.assertEqual(
            self.card._meta.get_field('decks').verbose_name,
            'decks',
        )

    def test_short_string_representation(self):
        '''Tests that the model string representaton returns as expected'''
        self.assertEqual(
            str(self.card),
            'This is a question (freeform)'
        )

    def test_long_string_representation(self):
        question = self.card.question_parts.all().first()
        question.text = 'a' * 50
        question.save()

        self.assertEqual(
            str(self.card),
            'aaaaaaaaaaaaaaaaaaaaaaaaaa... (freeform)'
        )

    # TODO: Add other string tests for MC and matching questions
