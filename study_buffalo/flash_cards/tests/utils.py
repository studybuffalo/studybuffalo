from flash_cards.models import PartContainer, TextPart

def create_text_part():
    new_text_part = TextPart.objects.create(
        text='This is test text.',
        order=1,
        container=PartContainer.objects.create()
    )

    return new_text_part
