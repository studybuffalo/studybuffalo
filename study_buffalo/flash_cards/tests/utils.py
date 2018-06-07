from django.contrib.auth import get_user_model

from flash_cards import models

def create_user():
    # user = apps.get_model('users', settings.AUTH_USER_MODEL).objects.create()
    user = get_user_model().objects.create()
    user.username = 'Regular User'
    user.set_password('abcd123456')
    user.is_superuser = False
    user.is_staff = False
    user.is_active = True
    user.save()

    return user

def create_tag():
    tag = models.Tag.objects.create(
        tag_name='cardiology',
    )

    return tag

def create_synonym():
    tag = create_tag()
    synonym = models.Synonym.objects.create(
        tag=tag,
        synonym_name='cardio',
    )

    return synonym

def create_deck(deck_name, description):
    return models.Deck.objects.create(
        deck_name=deck_name,
        description=description,
    )

def create_card():
    return models.Card.objects.create()

def create_question_part(text):
    card = create_card()

    return models.QuestionPart.objects.create(
        card=card,
        media_type='t',
        text=text,
        order=1,
    )

def create_media_part():
    return None

def create_multiple_choice_answer():
    card = create_card()

    return models.MultipleChoiceAnswer.objects.create(
        card=card,
        order=1,
        correct=False,
    )

def create_multiple_choice_answer_part(text):
    multiple_choice_answer = create_multiple_choice_answer()

    return models.MultipleChoiceAnswerPart.objects.create(
        multiple_choice_answer=multiple_choice_answer,
        media_type='t',
        text=text,
        order=1,
    )

def create_matching_answer():
    card = create_card()

    return models.MatchingAnswer.objects.create(
        card=card,
        side='l',
        order=1,
        pair=None,
    )

def create_matching_answer_part(text):
    matching_answer = create_matching_answer()

    return models.MatchingAnswerPart.objects.create(
        matching_answer=matching_answer,
        media_type='t',
        text=text,
        order=1,
    )

def create_freeform_answer_part(text):
    card = create_card()

    return models.FreeformAnswerPart.objects.create(
        media_type='t',
        text=text,
        order=1,
        card=card,
    )

def create_rationale_part(text):
    card = create_card()

    return models.RationalePart.objects.create(
        media_type='t',
        text=text,
        order=1,
        card=card,
    )

def create_reference():
    card = create_card()

    reference = models.Reference.objects.create(
        card=card,
        reference='This is a reference',
    )

    return reference

def create_card_deck_match(card, deck):
    return models.CardDeck.objects.create(
        card=card,
        deck=deck,
    )

def create_card_tag_match(card, tag):
    return models.CardTag.objects.create(
        card=card,
        tag=tag,
    )

def create_deck_stats():
    return models.DeckStats.objects.create(
        user=create_user(),
        deck=create_deck('Cardiology', 'A cardiology deck'),
        number_questions=3,
        number_correct=1,
        number_partially_correct=1,
        number_incorrect=1,
    )

def create_user_stats():
    return models.UserStats.objects.create(
        user=create_user(),
        number_decks=10,
        number_questions=60,
        number_correct=30,
        number_partially_correct=20,
        number_incorrect=10,
    )

def create_multiple_choice_card():
    # Create a card
    card = create_card()

    # Adding a question to the card
    models.QuestionPart.objects.create(
        card=card,
        media_type='t',
        text='This is a question',
        order=1,
    )

    # Add answers to the card
    answer_1 = models.MultipleChoiceAnswer.objects.create(
        card=card,
        order=1,
        correct=False,
    )
    models.MultipleChoiceAnswerPart.objects.create(
        multiple_choice_answer=answer_1,
        order=1,
        media_type='t',
        text='This is multiple choice answer 1',
        media=None,
    )

    answer_2 = models.MultipleChoiceAnswer.objects.create(
        card=card,
        order=2,
        correct=True,
    )
    models.MultipleChoiceAnswerPart.objects.create(
        multiple_choice_answer=answer_2,
        order=1,
        media_type='t',
        text='This is multiple choice answer 2',
        media=None,
    )

    return card

def create_matching_card():
    # Create a card
    card = create_card()

    # Adding a question to the card
    models.QuestionPart.objects.create(
        card=card,
        media_type='t',
        text='This is a question',
        order=1,
    )

    # Add answers to the card
    answer_1l = models.MatchingAnswer.objects.create(
        card=card,
        side='l',
        order=1,
        pair=None,
    )
    models.MatchingAnswerPart.objects.create(
        matching_answer=answer_1l,
        order=1,
        media_type='t',
        text='This is matching answer 1L',
        media=None,
    )

    answer_2l = models.MatchingAnswer.objects.create(
        card=card,
        side='l',
        order=2,
        pair=None,
    )
    models.MatchingAnswerPart.objects.create(
        matching_answer=answer_2l,
        order=1,
        media_type='t',
        text='This is matching answer 2L',
        media=None,
    )

    answer_1r = models.MatchingAnswer.objects.create(
        card=card,
        side='r',
        order=1,
        pair=None,
    )
    models.MatchingAnswerPart.objects.create(
        matching_answer=answer_1r,
        order=1,
        media_type='t',
        text='This is matching answer 1R',
        media=None,
    )

    answer_2r = models.MatchingAnswer.objects.create(
        card=card,
        side='r',
        order=2,
        pair=None,
    )
    models.MatchingAnswerPart.objects.create(
        matching_answer=answer_2r,
        order=1,
        media_type='t',
        text='This is matching answer 2R',
        media=None,
    )

    return card

def create_freeform_card():
    # Create a card
    card = create_card()

    # Adding a question to the card
    models.QuestionPart.objects.create(
        card=card,
        media_type='t',
        text='This is a question',
        order=1,
    )

    # Adding a freeform answer to the card
    models.FreeformAnswerPart.objects.create(
        card=card,
        media_type='t',
        text='This is a freeform answer',
        order=1,
    )

    return card

def create_card_feedback():
    return models.CardFeedback.objects.create(
        user=create_user(),
        comment='This is a feedback comment',
        card=create_freeform_card(),
    )

def create_deck_feedback():
    return models.DeckFeedback.objects.create(
        user=create_user(),
        comment='This is a feedback comment',
        deck=create_deck('Cardiology', 'A cardiology deck'),
    )

def create_card_post_data():
    deck = models.Deck.objects.create(
        deck_name='Cardiology Study Deck',
        description='A cardiology deck'
    )
    tag = models.Tag.objects.create(tag_name='cardiology')
    models.Synonym.objects.create(tag=tag, synonym_name='cardiology')

    return {
        'question_parts': [
            {
                'order': 1,
                'media_type': 't',
                'text': 'This is question text',
                'media': None,
            },
        ],
        'freeform_answer_parts': [
            {
                'order': 1,
                'media_type': 't',
                'text': 'This is freeform answer text',
                'media': None,
            },
            {
                'order': 2,
                'media_type': 't',
                'text': 'This is some more text',
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
        'decks': [
            {'id': deck.id},
        ],
        'tags': [
            {'tag_name': tag.tag_name},
        ],
    }
