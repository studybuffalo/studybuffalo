"""Factories for testing the Play app."""
import factory

from django.utils import timezone
from play import models


class CategoryFactory(factory.django.DjangoModelFactory):
    """Factory to generate a Category."""
    category = factory.Sequence(lambda n: f'Category {n}')

    class Meta:
        model = models.Category
        django_get_or_create = ('category',)


class PlayPageFactory(factory.django.DjangoModelFactory):
    """Factory to generate a PlayPage."""
    title = factory.Sequence(lambda n: f'Title {n}')
    date = timezone.now()
    category = factory.SubFactory(CategoryFactory)
    release_date = timezone.now()

    class Meta:
        model = models.PlayPage
        django_get_or_create = ('title', 'category')


class PlayImageFactory(factory.django.DjangoModelFactory):
    """Factory to generate a PlayImage."""
    title = factory.Sequence(lambda n: f'Image {n}')
    type = 'i'
    original_image = factory.django.ImageField()
    alt_text = factory.Sequence(lambda n: f'Alt {n}')
    description = factory.Sequence(lambda n: f'Description {n}')
    page = factory.SubFactory(PlayPageFactory)
    ordering = factory.Sequence(lambda n: n)


class PlayAudioFactory(factory.django.DjangoModelFactory):
    """Factory to generate a PlayImage."""
    title = factory.Sequence(lambda n: f'Image {n}')
    type = 'a'
    audio = factory.django.FileField(filename='audio.mp3')
    alt_text = factory.Sequence(lambda n: f'Alt {n}')
    description = factory.Sequence(lambda n: f'Description {n}')
    page = factory.SubFactory(PlayPageFactory)
    ordering = factory.Sequence(lambda n: n)
