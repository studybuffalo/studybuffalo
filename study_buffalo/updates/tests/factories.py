"""Factories for testing the Updates app."""
import factory

from django.utils import timezone
from updates import models


class UpdateFactory(factory.django.DjangoModelFactory):
    """Factory to generate a Publication."""
    title = factory.Sequence(lambda n: f'Title {n}')
    background = factory.django.ImageField()
    icon = factory.django.ImageField()
    html = factory.Sequence(lambda n: f'<html>{n}</html>')
    start_date = timezone.now()
    end_date = None
    priority = factory.Sequence(lambda n: n)

    class Meta:
        model = models.Update
        django_get_or_create = ('title', 'start_date')
