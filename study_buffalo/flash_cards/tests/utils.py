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

    # Create Answer #1
    part_container_1L = models.PartContainer.objects.create()
    models.TextPart.objects.create(
        text="Left: Answer 1",
        order=1,
        container=part_container_1L,
    )
    answer_1L = models.MatchingAnswer.objects.create(
        container=container,
        part_container=part_container_1L,
        side='l',
        order=1,
        pair=None,
    )
