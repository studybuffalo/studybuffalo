from django.test import TestCase

from flash_cards import models
from flash_cards.api import serializers

class CardSerializerTest(TestCase):
    def setUp(self):
        # Populate initial database details
        deck = models.Deck.objects.create(
            deck_name='Cardiology Study Deck',
        )
        tag = models.Tag.objects.create(
            tag_name='cardiology',
        )
        models.Synonym.objects.create(
            tag=tag,
            synonym_name='cardio',
        )

        # Setup a base data set
        data = {
            'question_parts': [
                {
                    'order': 1,
                    'media_type': 't',
                    'text': 'This is question text',
                    'media': None,
                },
            ],
            'rationale_parts': [
                {
                    'order': 1,
                    'media_type': 't',
                    'text': 'This is rationale text',
                    'media': None,
                },
            ],
            'reviewed': False,
            'active': True,
            'date_modified': '2018-01-01T12:00:00.000000Z',
            'date_reviewed': '2018-01-02T12:00:00.000000Z',
            'references': [
                {'reference': 'This is reference text'},
            ],
            'tags': [
                {'tag_name': 'cardio'},
            ],
            'decks': [
                {'id': deck.id},
            ]
        }

        # Create a multiple choice answer dataset
        multiple_choice_data = dict(data)
        multiple_choice_data['multiple_choice_answers'] = [
            {
                'order': 1,
                'correct': False,
                'multiple_choice_answer_parts': [
                    {
                        'order': 1,
                        'media_type': 't',
                        'text': 'This is multiple choice answer 1',
                        'media': None,
                    }
                ]
            },
            {
                'order': 2,
                'correct': True,
                'multiple_choice_answer_parts': [
                    {
                        'order': 1,
                        'media_type': 't',
                        'text': 'This is multiple choice answer 2',
                        'media': None,
                    }
                ]
            },
            {
                'order': 3,
                'correct': False,
                'multiple_choice_answer_parts': [
                    {
                        'order': 1,
                        'media_type': 't',
                        'text': 'This is multiple choice answer 3',
                        'media': None,
                    }
                ]
            }
        ]

        # Create a matching answer dataset
        matching_data = dict(data)
        matching_data['matching_answers'] = [
            {
                'side': 'l',
                'order': 1,
                'pair': None,
                'matching_answer_parts': [
                    {
                        'order': 1,
                        'media_type': 't',
                        'text': 'This is matching answer 1L',
                        'media': None,
                    }
                ]
            },
            {
                'side': 'l',
                'order': 2,
                'pair': None,
                'matching_answer_parts': [
                    {
                        'order': 1,
                        'media_type': 't',
                        'text': 'This is matching answer 2L',
                        'media': None,
                    }
                ]
            },
            {
                'side': 'r',
                'order': 1,
                'pair': None,
                'matching_answer_parts': [
                    {
                        'order': 1,
                        'media_type': 't',
                        'text': 'This is matching answer 1R',
                        'media': None,
                    }
                ]
            },
            {
                'side': 'r',
                'order': 2,
                'pair': None,
                'matching_answer_parts': [
                    {
                        'order': 1,
                        'media_type': 't',
                        'text': 'This is matching answer 2R',
                        'media': None,
                    }
                ]
            },
        ]

        # Create a freeform answer dataset
        freeform_data = dict(data)
        freeform_data['freeform_answer_parts'] = [
            {
                'order': 1,
                'media_type': 't',
                'text': 'This is freeform answer text',
                'media': None,
            }
        ]

        self.multiple_choice_data = multiple_choice_data
        self.matching_data = matching_data
        self.freeform_data = freeform_data

    def test_accepts_valid_multiple_choice_data(self):
        serializer = serializers.CardSerializer(data=self.multiple_choice_data)

        self.assertTrue(serializer.is_valid())

    def test_expected_multiple_choice_fields(self):
        serializer = serializers.CardSerializer(data=self.multiple_choice_data)

        self.assertTrue(serializer.is_valid())

        self.assertCountEqual(
            serializer.validated_data.keys(),
            [
                'question_parts', 'multiple_choice_answers', 'rationale_parts',
                'reviewed', 'active', 'date_modified', 'date_reviewed',
                'references', 'tags', 'decks',
            ]
        )

    def test_accepts_valid_matching_data(self):
        serializer = serializers.CardSerializer(data=self.matching_data)

        self.assertTrue(serializer.is_valid())

    def test_expected_matching_fields(self):
        serializer = serializers.CardSerializer(data=self.matching_data)

        self.assertTrue(serializer.is_valid())

        self.assertCountEqual(
            serializer.validated_data.keys(),
            [
                'question_parts', 'matching_answers', 'rationale_parts',
                'reviewed', 'active', 'date_modified', 'date_reviewed',
                'references', 'tags', 'decks',
            ]
        )

    def test_accepts_valid_freeform_data(self):
        serializer = serializers.CardSerializer(data=self.freeform_data)

        self.assertTrue(serializer.is_valid())

    def test_expected_freeform_fields(self):
        serializer = serializers.CardSerializer(data=self.freeform_data)

        self.assertTrue(serializer.is_valid())

        self.assertCountEqual(
            serializer.validated_data.keys(),
            [
                'question_parts', 'freeform_answer_parts', 'rationale_parts',
                'reviewed', 'active', 'date_modified', 'date_reviewed',
                'references', 'tags', 'decks',
            ]
        )

    def test_multiple_choice_relationships_created(self):
        # Get current counts
        question_total = models.QuestionPart.objects.all().count()
        answer_total = models.MultipleChoiceAnswer.objects.all().count()
        answer_part_total = models.MultipleChoiceAnswerPart.objects.all().count()
        rationale_total = models.RationalePart.objects.all().count()
        card_tag_total = models.CardTag.objects.all().count()
        deck_tag_total = models.CardDeck.objects.all().count()

        # Save models
        serializer = serializers.CardSerializer(data=self.multiple_choice_data)

        self.assertTrue(serializer.is_valid())

        serializer.save()

        # Compared model counts
        self.assertEqual(
            models.QuestionPart.objects.all().count(),
            question_total + 1
        )

        self.assertEqual(
            models.MultipleChoiceAnswer.objects.all().count(),
            answer_total + 3
        )

        self.assertEqual(
            models.MultipleChoiceAnswerPart.objects.all().count(),
            answer_part_total + 3
        )

        self.assertEqual(
            models.RationalePart.objects.all().count(),
            rationale_total + 1
        )

        self.assertEqual(
            models.CardTag.objects.all().count(),
            card_tag_total + 1
        )

        self.assertEqual(
            models.CardDeck.objects.all().count(),
            deck_tag_total + 1
        )

    def test_freeform_relationships_created(self):
        # Get current counts
        question_total = models.QuestionPart.objects.all().count()
        freeform_total = models.FreeformAnswerPart.objects.all().count()
        rationale_total = models.RationalePart.objects.all().count()
        card_tag_total = models.CardTag.objects.all().count()
        deck_tag_total = models.CardDeck.objects.all().count()

        # Save models
        serializer = serializers.CardSerializer(data=self.freeform_data)

        self.assertTrue(serializer.is_valid())

        serializer.save()

        # Compared model counts
        self.assertEqual(
            models.QuestionPart.objects.all().count(),
            question_total + 1
        )

        self.assertEqual(
            models.FreeformAnswerPart.objects.all().count(),
            freeform_total + 1
        )

        self.assertEqual(
            models.RationalePart.objects.all().count(),
            rationale_total + 1
        )

        self.assertEqual(
            models.CardTag.objects.all().count(),
            card_tag_total + 1
        )

        self.assertEqual(
            models.CardDeck.objects.all().count(),
            deck_tag_total + 1
        )

    def test_old_tags_retrieved(self):
        # Get current counts
        tag_total = models.Tag.objects.all().count()
        synonym_total = models.Synonym.objects.all().count()

        # Save models
        serializer = serializers.CardSerializer(data=self.freeform_data)

        self.assertTrue(serializer.is_valid())

        serializer.save()

        # Compared model counts
        self.assertEqual(
            models.Tag.objects.all().count(),
            tag_total
        )

        self.assertEqual(
            models.Synonym.objects.all().count(),
            synonym_total
        )

    def test_new_tags_created(self):
        # Get current counts
        tag_total = models.Tag.objects.all().count()
        synonym_total = models.Synonym.objects.all().count()

        # Specify new tag
        data = self.freeform_data
        data['tags'][0]['tag_name'] = 'neurology'

        # Save models
        serializer = serializers.CardSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        serializer.save()

        # Compared model counts
        self.assertEqual(
            models.Tag.objects.all().count(),
            tag_total + 1
        )

        self.assertEqual(
            models.Synonym.objects.all().count(),
            synonym_total + 1
        )

    # TODO: Build tests for other answer types
    # TODO: Build tests for more varied parts
