"""Factories for testing the Study app."""
import factory

from django.utils import timezone

from study import models
from users.tests.factories import UserFactory


class GuideFactory(factory.django.DjangoModelFactory):
    """Factory to generate a Guide."""
    title = factory.Sequence(lambda n: f'Title {n}')
    short_description = factory.Sequence(lambda n: f'Short {n}')
    long_description = factory.Sequence(lambda n: f'Long {n}')
    date_original = timezone.now()
    last_update = timezone.now()
    permissions = None

    class Meta:
        model = models.Guide
        django_get_or_create = ('title', 'short_description')


class BountyFactory(factory.django.DjangoModelFactory):
    """Factory to generate a Bounty."""
    study_guide = factory.SubFactory(GuideFactory)
    bounty_status = 'o'
    bounty_amount = factory.Sequence(lambda n: n)
    bounty_details = factory.Sequence(lambda n: f'Details {n}')

    class Meta:
        model = models.Bounty
        django_get_or_create = ('bounty_details',)


class BountyAssignment(factory.django.DjangoModelFactory):
    """Factory to generate a BountyAssignment."""
    bounty = factory.SubFactory(BountyFactory)
    assignment_status = 'i'
    assigned_user = factory.SubFactory(UserFactory)
    proportion = factory.Sequence(lambda n: f'Details {n}')

    class Meta:
        model = models.Bounty


class HTMLGuideFactory(factory.django.DjangoModelFactory):
    """Factory to generate a HTMLGuide."""
    study_guide = factory.SubFactory(GuideFactory)
    html = factory.Sequence(lambda n: f'<p>HTML {n}</p>')

    class Meta:
        model = models.HTMLGuide
        django_get_or_create = ('html',)


class DocumentGuideFactory(factory.django.DjangoModelFactory):
    """Factory to generate a PlayImage."""
    study_guide = factory.SubFactory(GuideFactory)
    document = factory.django.FileField(filename='Example Document.txt')

    class Meta:
        model = models.DocumentGuide
        django_get_or_create = ('document',)
