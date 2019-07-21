"""Factories to create working user and related models."""
import factory

from rdrhc_calendar.models import CalendarUser, ShiftCode, Shift, MissingShiftCode
from users.tests.factories import UserFactory

class CalendarUserFactory(factory.django.DjangoModelFactory):
    sb_user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'name - {n}')
    schedule_name = factory.Sequence(lambda n: f'schedule name - {n}')
    calendar_name = factory.Sequence(lambda n: f'calendar name - {n}')
    role = 'p'
    reminder = factory.Sequence(lambda n: int(n))

    class Meta:
        model = CalendarUser
        django_get_or_create = ('name',)

class ShiftCodeFactory(factory.django.DjangoModelFactory):
    code = factory.Sequence(lambda n: 'A - {%s}' % n)
    sb_user = factory.SubFactory(UserFactory)
    role = 'p'
    monday_start = factory.Sequence(lambda n: '01:%02d' % n)
    monday_duration = factory.Sequence(lambda n: '%s.%s' % (n, n))
    tuesday_start = factory.Sequence(lambda n: '02:%02d' % n)
    tuesday_duration = factory.Sequence(lambda n: '%s.%s' % (n, n))
    wednesday_start = factory.Sequence(lambda n: '03:%02d' % n)
    wednesday_duration = factory.Sequence(lambda n: '%s.%s' % (n, n))
    thursday_start = factory.Sequence(lambda n: '04:%02d' % n)
    thursday_duration = factory.Sequence(lambda n: '%s.%s' % (n, n))
    friday_start = factory.Sequence(lambda n: '05:%02d' % n)
    friday_duration = factory.Sequence(lambda n: '%s.%s' % (n, n))
    saturday_start = factory.Sequence(lambda n: '06:%02d' % n)
    saturday_duration = factory.Sequence(lambda n: '%s.%s' % (n, n))
    sunday_start = factory.Sequence(lambda n: '07:%02d' % n)
    sunday_duration = factory.Sequence(lambda n: '%s.%s' % (n, n))
    stat_start = factory.Sequence(lambda n: '08:%02d' % n)
    stat_duration = factory.Sequence(lambda n: '%s.%s' % (n, n))

    class Meta:
        model = ShiftCode
        django_get_or_create = ('code', 'sb_user', 'role')

class ShiftFactory(factory.django.DjangoModelFactory):
    sb_user = factory.SubFactory(UserFactory)
    shift_code = factory.SubFactory(ShiftCodeFactory)
    date = factory.Sequence(lambda n: '20%02d-01-01' % n)
    text_shift_code = factory.Sequence(lambda n: 'A%s' % n)

    class Meta:
        model = Shift

class MissingShiftCodeFactory(factory.django.DjangoModelFactory):
    code = factory.Sequence(lambda n: 'A%s' % n)
    role = 'p'

    class Meta:
        model = MissingShiftCode
