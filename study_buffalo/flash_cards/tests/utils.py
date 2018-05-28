from flash_cards import models

def create_text_part(text):
    new_text_part = models.TextPart.objects.create(
        text=text,
        order=1,
        container=models.PartContainer.objects.create()
    )

    return new_text_part

def create_media_part():
    return None

def create_multiple_choice_answers():
    container = models.MultipleChoiceContainer.objects.create()

    # Create Answer #1
    part_container_1 = models.PartContainer.objects.create()
    models.TextPart.objects.create(
        text="Answer 1",
        order=1,
        container=part_container_1,
    )
    models.MultipleChoiceAnswer.objects.create(
        container=container,
        part_container=part_container_1,
        order=1,
        correct=False,
    )

    # Create Answer #2
    part_container_2 = models.PartContainer.objects.create()
    models.TextPart.objects.create(
        text="Answer 2",
        order=1,
        container=part_container_2,
    )
    models.MultipleChoiceAnswer.objects.create(
        container=container,
        part_container=part_container_2,
        order=2,
        correct=True,
    )

    # Create Answer #3
    part_container_3 = models.PartContainer.objects.create()
    models.TextPart.objects.create(
        text="Answer 3",
        order=1,
        container=part_container_3,
    )
    models.MultipleChoiceAnswer.objects.create(
        container=container,
        part_container=part_container_3,
        order=3,
        correct=False,
    )

    return container

def create_matching_answers():
    container = models.MatchingContainer.objects.create()

    # Create Answer #1L
    part_container_1L = models.PartContainer.objects.create()
    models.TextPart.objects.create(
        text="Left: Answer 1",
        order=1,
        container=part_container_1L,
    )
    answer_1L = models.MatchingAnswer.objects.create(
        question_container=container,
        part_container=part_container_1L,
        side='l',
        order=1,
        pair=None,
    )

    # Create Answer #1R
    part_container_1R = models.PartContainer.objects.create()
    models.TextPart.objects.create(
        text="Right: Answer 1",
        order=1,
        container=part_container_1R,
    )
    answer_1R = models.MatchingAnswer.objects.create(
        question_container=container,
        part_container=part_container_1R,
        side='r',
        order=1,
        pair=None,
    )

    # Create Answer #2L
    part_container_2L = models.PartContainer.objects.create()
    models.TextPart.objects.create(
        text="Left: Answer 2",
        order=1,
        container=part_container_2L,
    )
    answer_2L = models.MatchingAnswer.objects.create(
        question_container=container,
        part_container=part_container_2L,
        side='l',
        order=2,
        pair=None,
    )

    # Create Answer #2R
    part_container_2R = models.PartContainer.objects.create()
    models.TextPart.objects.create(
        text="Right: Answer 2",
        order=1,
        container=part_container_2R,
    )
    answer_2R = models.MatchingAnswer.objects.create(
        question_container=container,
        part_container=part_container_2R,
        side='r',
        order=2,
        pair=None,
    )

    # Create Answer #3L
    part_container_3L = models.PartContainer.objects.create()
    models.TextPart.objects.create(
        text="Left: Answer 3",
        order=1,
        container=part_container_3L,
    )
    answer_3L = models.MatchingAnswer.objects.create(
        question_container=container,
        part_container=part_container_3L,
        side='l',
        order=3,
        pair=None,
    )

    # Create Answer #3R
    part_container_3R = models.PartContainer.objects.create()
    models.TextPart.objects.create(
        text="Right: Answer 1",
        order=1,
        container=part_container_1R,
    )
    answer_3R = models.MatchingAnswer.objects.create(
        question_container=container,
        part_container=part_container_3R,
        side='r',
        order=3,
        pair=None,
    )

    # Matching Pairs
    answer_1L.pair = answer_1R
    answer_1L.save()
    answer_1R.pair = answer_1L
    answer_1R.save()
    answer_2L.pair = answer_2R
    answer_2L.save()
    answer_2R.pair = answer_2L
    answer_2R.save()
    answer_3L.pair = answer_3R
    answer_3L.save()
    answer_3R.pair = answer_3L
    answer_3R.save()

    return container

def create_multiple_choice_card():
    card = models.Card.objects.create()

    return card

def create_matching_card():
    card = models.Card.objects.create()

    return card

def create_freeform_card():
    # Setup required parts
    question_text = create_text_part('This is a question')
    answer_text = create_text_part('This is the answer')
    rationale = create_text_part('This is the rationale')

    card = models.Card.objects.create(
        question=question_text.container,
        answer_multiple_choice=None,
        answer_matching=None,
        answer_freeform=answer_text.container,
        rationale=rationale.container,
    )

    return card

def create_reference():
    card = create_freeform_card()
    reference = models.Reference.objects.create(
        card=card,
        reference='This is a reference',
    )

    return reference

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
    return models.Deck(
        deck_name=deck_name,
    )
