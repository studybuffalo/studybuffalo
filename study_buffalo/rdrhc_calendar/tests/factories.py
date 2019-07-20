"""Factories to create working user and related models."""
import factory

from rdrhc_calendar.models import CalendarUser
from users.tests.factories import UserFactory

class CalendarUserFactory(factory.django.DjangoModelFactory):
    sb_user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'name - {n}')
    schedule_name = factory.Sequence(lambda n: f'schedule name - {n}')
    calendar_name = factory.Sequence(lambda n: f'calendar name - {n}')
    role = 'p'

    class Meta:
        model = CalendarUser
        django_get_or_create = ('name',)
