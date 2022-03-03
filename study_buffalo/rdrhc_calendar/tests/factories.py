"""Factories to create working user and related models."""
import factory

from rdrhc_calendar.models import CalendarUser, ShiftCode, Shift, MissingShiftCode
from users.tests.factories import UserFactory

class CalendarUserFactory(factory.django.DjangoModelFactory):
    """Factory to generate Calendar User."""
    sb_user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'name - {n}')
    schedule_name = factory.Sequence(lambda n: f'schedule name - {n}')
    calendar_name = factory.Sequence(lambda n: f'calendar name - {n}')
    role = 'p'
    reminder = factory.Sequence(lambda n: int(n)) # pylint: disable=unnecessary-lambda

    class Meta:
        model = CalendarUser
        django_get_or_create = ('name',)

class ShiftCodeFactory(factory.django.DjangoModelFactory):
    """Factory to generate a Shift Code."""
    code = factory.Sequence(lambda n: f'A - {n}')
    sb_user = factory.SubFactory(UserFactory)
    role = 'p'
    monday_start = factory.Sequence(lambda n: f'01:{n:02}')
    monday_duration = factory.Sequence(lambda n: f'{n}.{n}')
    tuesday_start = factory.Sequence(lambda n: f'02:{n:02}')
    tuesday_duration = factory.Sequence(lambda n: f'{n}.{n}')
    wednesday_start = factory.Sequence(lambda n: f'03:{n:02}')
    wednesday_duration = factory.Sequence(lambda n: f'{n}.{n}')
    thursday_start = factory.Sequence(lambda n: f'04:{n:02}')
    thursday_duration = factory.Sequence(lambda n: f'{n}.{n}')
    friday_start = factory.Sequence(lambda n: f'05:{n:02}')
    friday_duration = factory.Sequence(lambda n: f'{n}.{n}')
    saturday_start = factory.Sequence(lambda n: f'06:{n:02}')
    saturday_duration = factory.Sequence(lambda n: f'{n}.{n}')
    sunday_start = factory.Sequence(lambda n: f'07:{n:02}')
    sunday_duration = factory.Sequence(lambda n: f'{n}.{n}')
    stat_start = factory.Sequence(lambda n: f'08:{n:02}')
    stat_duration = factory.Sequence(lambda n: f'{n}.{n}')

    class Meta:
        model = ShiftCode
        django_get_or_create = ('code', 'sb_user', 'role')

class ShiftFactory(factory.django.DjangoModelFactory):
    """Factory to generate a Shift."""
    sb_user = factory.SubFactory(UserFactory)
    shift_code = factory.SubFactory(ShiftCodeFactory)
    date = factory.Sequence(lambda n: f'20{n:02}-01-01')
    text_shift_code = factory.Sequence(lambda n: f'A{n}')

    class Meta:
        model = Shift

class MissingShiftCodeFactory(factory.django.DjangoModelFactory):
    """Factory to generate a Missing Shift Code."""
    code = factory.Sequence(lambda n: f'A{n}')
    role = 'p'

    class Meta:
        model = MissingShiftCode
