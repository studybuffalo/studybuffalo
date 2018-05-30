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

# def create_multiple_choice_answers():
#     container = models.MultipleChoiceContainer.objects.create()

#     # Create Answer #1
#     part_container_1 = models.PartContainer.objects.create()
#     models.TextPart.objects.create(
#         text="Answer 1",
#         order=1,
#         container=part_container_1,
#     )
#     models.MultipleChoiceAnswer.objects.create(
#         container=container,
#         part_container=part_container_1,
#         order=1,
#         correct=False,
#     )

#     # Create Answer #2
#     part_container_2 = models.PartContainer.objects.create()
#     models.TextPart.objects.create(
#         text="Answer 2",
#         order=1,
#         container=part_container_2,
#     )
#     models.MultipleChoiceAnswer.objects.create(
#         container=container,
#         part_container=part_container_2,
#         order=2,
#         correct=True,
#     )

#     # Create Answer #3
#     part_container_3 = models.PartContainer.objects.create()
#     models.TextPart.objects.create(
#         text="Answer 3",
#         order=1,
#         container=part_container_3,
#     )
#     models.MultipleChoiceAnswer.objects.create(
#         container=container,
#         part_container=part_container_3,
#         order=3,
#         correct=False,
#     )

#     return container

# def create_matching_answers():
#     container = models.MatchingContainer.objects.create()

#     # Create Answer #1L
#     part_container_1L = models.PartContainer.objects.create()
#     models.TextPart.objects.create(
#         text="Left: Answer 1",
#         order=1,
#         container=part_container_1L,
#     )
#     answer_1L = models.MatchingAnswer.objects.create(
#         question_container=container,
#         part_container=part_container_1L,
#         side='l',
#         order=1,
#         pair=None,
#     )

#     # Create Answer #1R
#     part_container_1R = models.PartContainer.objects.create()
#     models.TextPart.objects.create(
#         text="Right: Answer 1",
#         order=1,
#         container=part_container_1R,
#     )
#     answer_1R = models.MatchingAnswer.objects.create(
#         question_container=container,
#         part_container=part_container_1R,
#         side='r',
#         order=1,
#         pair=None,
#     )

#     # Create Answer #2L
#     part_container_2L = models.PartContainer.objects.create()
#     models.TextPart.objects.create(
#         text="Left: Answer 2",
#         order=1,
#         container=part_container_2L,
#     )
#     answer_2L = models.MatchingAnswer.objects.create(
#         question_container=container,
#         part_container=part_container_2L,
#         side='l',
#         order=2,
#         pair=None,
#     )

#     # Create Answer #2R
#     part_container_2R = models.PartContainer.objects.create()
#     models.TextPart.objects.create(
#         text="Right: Answer 2",
#         order=1,
#         container=part_container_2R,
#     )
#     answer_2R = models.MatchingAnswer.objects.create(
#         question_container=container,
#         part_container=part_container_2R,
#         side='r',
#         order=2,
#         pair=None,
#     )

#     # Create Answer #3L
#     part_container_3L = models.PartContainer.objects.create()
#     models.TextPart.objects.create(
#         text="Left: Answer 3",
#         order=1,
#         container=part_container_3L,
#     )
#     answer_3L = models.MatchingAnswer.objects.create(
#         question_container=container,
#         part_container=part_container_3L,
#         side='l',
#         order=3,
#         pair=None,
#     )

#     # Create Answer #3R
#     part_container_3R = models.PartContainer.objects.create()
#     models.TextPart.objects.create(
#         text="Right: Answer 1",
#         order=1,
#         container=part_container_1R,
#     )
#     answer_3R = models.MatchingAnswer.objects.create(
#         question_container=container,
#         part_container=part_container_3R,
#         side='r',
#         order=3,
#         pair=None,
#     )

#     # Matching Pairs
#     answer_1L.pair = answer_1R
#     answer_1L.save()
#     answer_1R.pair = answer_1L
#     answer_1R.save()
#     answer_2L.pair = answer_2R
#     answer_2L.save()
#     answer_2R.pair = answer_2L
#     answer_2R.save()
#     answer_3L.pair = answer_3R
#     answer_3L.save()
#     answer_3R.pair = answer_3L
#     answer_3R.save()

#     return container

# def create_multiple_choice_card():
#     card = models.Card.objects.create()

#     return card

# def create_matching_card():
#     card = models.Card.objects.create()

#     return card

# def create_freeform_card():
#     # Setup required parts
#     question_text = create_text_part('This is a question')
#     answer_text = create_text_part('This is the answer')
#     rationale = create_text_part('This is the rationale')

#     card = models.Card.objects.create(
#         question=question_text.container,
#         answer_multiple_choice=None,
#         answer_matching=None,
#         answer_freeform=answer_text.container,
#         rationale=rationale.container,
#     )

#     return card

# def create_reference():
#     card = create_freeform_card()
#     reference = models.Reference.objects.create(
#         card=card,
#         reference='This is a reference',
#     )

#     return reference

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

# def create_card_feedback():
#     return models.CardFeedback.objects.create(
#         user=create_user(),
#         comment='This is a feedback comment',
#         card=create_freeform_card(),
#     )

# def create_deck_feedback():
    # return models.DeckFeedback.objects.create(
    #     user=create_user(),
    #     comment='This is a feedback comment',
    #     deck=create_deck('Cardiology'),
    # )
