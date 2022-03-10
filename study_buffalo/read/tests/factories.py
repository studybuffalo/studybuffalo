"""Factories for testing the Read app."""
import factory

from django.utils import timezone
from read import models


class PublicationFactory(factory.django.DjangoModelFactory):
    """Factory to generate a Publication."""
    title = factory.Sequence(lambda n: f'Title {n}')
    description = factory.Sequence(lambda n: f'Description {n}')
    date_published = timezone.now()

    class Meta:
        model = models.Publication
        django_get_or_create = ('title', 'description')


class HTMLPublicationFactory(factory.django.DjangoModelFactory):
    """Factory to generate a HTMLPublication."""
    publication = factory.SubFactory(PublicationFactory)
    html = factory.Sequence(lambda n: f'<p>HTML {n}</p>')

    class Meta:
        model = models.HTMLPublication
        django_get_or_create = ('html',)


class DocumentPublicationFactory(factory.django.DjangoModelFactory):
    """Factory to generate a PlayImage."""
    publication = factory.SubFactory(PublicationFactory)
    document = factory.django.FileField(filename='Example Document.txt')

    class Meta:
        model = models.DocumentPublication
        django_get_or_create = ('document',)
