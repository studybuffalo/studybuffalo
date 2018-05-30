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

def create_deck(deck_name):
    return models.Deck.objects.create(
        deck_name=deck_name,
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
        deck=create_deck('Cardiology'),
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

def create_card_feedback():
    return models.CardFeedback.objects.create(
        user=create_user(),
        comment='This is a feedback comment',
        card=create_card(),
    )

def create_deck_feedback():
    return models.DeckFeedback.objects.create(
        user=create_user(),
        comment='This is a feedback comment',
        deck=create_deck('Cardiology'),
    )
