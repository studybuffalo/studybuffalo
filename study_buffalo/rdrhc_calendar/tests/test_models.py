"""Tests for the rdrhc_calendar models."""
from django.db import IntegrityError
from django.test import TestCase

from rdrhc_calendar import models

from .utils import create_user


class TestCalendarUser(TestCase):
    def setUp(self):
        self.calendar_user = models.CalendarUser.objects.create(
            sb_user=create_user(),
            name='Regular User',
            schedule_name='User',
            calendar_name='SecretCalendar',
            role='p',
            first_email_sent=False,
            full_day=False,
            reminder=0,
        )

    def test_labels(self):
        self.assertEqual(
            self.calendar_user._meta.get_field('id').verbose_name,
            'ID',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('sb_user').verbose_name,
            'SB user',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('name').verbose_name,
            'name',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('schedule_name').verbose_name,
            'schedule name',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('calendar_name').verbose_name,
            'calendar name',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('role').verbose_name,
            'role',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('first_email_sent').verbose_name,
            'first email sent',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('full_day').verbose_name,
            'full day',
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('reminder').verbose_name,
            'reminder',
        )

    def test_max_lengths(self):
        self.assertEqual(
            self.calendar_user._meta.get_field('name').max_length,
            25
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('schedule_name').max_length,
            25
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('calendar_name').max_length,
            50
        )
        self.assertEqual(
            self.calendar_user._meta.get_field('role').max_length,
            1
        )

    def test_role_choices(self):
        choices = self.calendar_user._meta.get_field('role').choices

        self.assertTrue(('a', 'Pharmacy Assistant') in choices)
        self.assertTrue(('p', 'Pharmacist') in choices)
        self.assertTrue(('t', 'Pharmacy Technician') in choices)

    def test_str(self):
        self.assertEqual(
            str(self.calendar_user),
            'p - Regular User'
        )

class TestStatHoliday(TestCase):
    def setUp(self):
        self.stat_holiday = models.StatHoliday.objects.create(
            date='2018-01-01',
        )

    def test_labels(self):
        self.assertEqual(
            self.stat_holiday._meta.get_field('date').verbose_name,
            'date',
        )

    def test_str(self):
        self.assertEqual(
            str(self.stat_holiday),
            '2018-01-01'
        )

class TestShiftCode(TestCase):
    def setUp(self):
        self.shift_code = models.ShiftCode.objects.create(
            code='A1',
            sb_user=create_user(),
            role='p',
            monday_start='01:00',
            monday_duration='1.1',
            tuesday_start='02:00',
            tuesday_duration='2.2',
            wednesday_start='03:00',
            wednesday_duration='3.3',
            thursday_start='04:00',
            thursday_duration='4.4',
            friday_start='05:00',
            friday_duration='5.5',
            saturday_start='06:00',
            saturday_duration='6.6',
            sunday_start='07:00',
            sunday_duration='7.7',
            stat_start='08:00',
            stat_duration='8.8',
        )

    def test_labels(self):
        self.assertEqual(
            self.shift_code._meta.get_field('code').verbose_name,
            'code',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('sb_user').verbose_name,
            'SB user',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('role').verbose_name,
            'role',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('monday_start').verbose_name,
            'monday start',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('monday_duration').verbose_name,
            'monday duration',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('tuesday_start').verbose_name,
            'tuesday start',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('tuesday_duration').verbose_name,
            'tuesday duration',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('wednesday_start').verbose_name,
            'wednesday start',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('wednesday_duration').verbose_name,
            'wednesday duration',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('thursday_start').verbose_name,
            'thursday start',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('thursday_duration').verbose_name,
            'thursday duration',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('friday_start').verbose_name,
            'friday start',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('friday_duration').verbose_name,
            'friday duration',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('saturday_start').verbose_name,
            'saturday start',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('saturday_duration').verbose_name,
            'saturday duration',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('sunday_start').verbose_name,
            'sunday start',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('sunday_duration').verbose_name,
            'sunday duration',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('stat_start').verbose_name,
            'stat start',
        )
        self.assertEqual(
            self.shift_code._meta.get_field('stat_duration').verbose_name,
            'stat duration',
        )

    def test_max_lengths(self):
        self.assertEqual(
            self.shift_code._meta.get_field('code').max_length,
            20
        )
        self.assertEqual(
            self.shift_code._meta.get_field('role').max_length,
            1
        )

    def test_decimal_maxes(self):
        self.assertEqual(
            self.shift_code._meta.get_field('monday_duration').decimal_places,
            2
        )
        self.assertEqual(
            self.shift_code._meta.get_field('monday_duration').max_digits,
            4
        )
        self.assertEqual(
            self.shift_code._meta.get_field('tuesday_duration').decimal_places,
            2
        )
        self.assertEqual(
            self.shift_code._meta.get_field('tuesday_duration').max_digits,
            4
        )
        self.assertEqual(
            self.shift_code._meta.get_field('wednesday_duration').decimal_places,
            2
        )
        self.assertEqual(
            self.shift_code._meta.get_field('wednesday_duration').max_digits,
            4
        )

        self.assertEqual(
            self.shift_code._meta.get_field('thursday_duration').decimal_places,
            2
        )
        self.assertEqual(
            self.shift_code._meta.get_field('thursday_duration').max_digits,
            4
        )

        self.assertEqual(
            self.shift_code._meta.get_field('friday_duration').decimal_places,
            2
        )
        self.assertEqual(
            self.shift_code._meta.get_field('friday_duration').max_digits,
            4
        )

        self.assertEqual(
            self.shift_code._meta.get_field('saturday_duration').decimal_places,
            2
        )
        self.assertEqual(
            self.shift_code._meta.get_field('saturday_duration').max_digits,
            4
        )

        self.assertEqual(
            self.shift_code._meta.get_field('sunday_duration').decimal_places,
            2
        )
        self.assertEqual(
            self.shift_code._meta.get_field('sunday_duration').max_digits,
            4
        )

        self.assertEqual(
            self.shift_code._meta.get_field('stat_duration').decimal_places,
            2
        )
        self.assertEqual(
            self.shift_code._meta.get_field('stat_duration').max_digits,
            4
        )

    def test_role_choices(self):
        choices = self.shift_code._meta.get_field('role').choices

        self.assertTrue(('a', 'Pharmacy Assistant') in choices)
        self.assertTrue(('p', 'Pharmacist') in choices)
        self.assertTrue(('t', 'Pharmacy Technician') in choices)

    def test_null_field_model_creation(self):
        try:
            shift_code = models.ShiftCode.objects.create(
                code='A1',
                role='p',
            )
        except IntegrityError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_unique_together_validation(self):
        try:
            models.ShiftCode.objects.create(
                code='A1',
                sb_user=self.shift_code.sb_user,
                role='p',
            )
        except IntegrityError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_str_with_user(self):
        self.assertEqual(
            str(self.shift_code),
            'Pharmacist - Regular User - A1'
        )

    def test_str_without_user(self):
        shift_code = models.ShiftCode.objects.create(
            code='A2',
            role='p',
        )
        self.assertEqual(
            str(shift_code),
            'Pharmacist - A2'
        )


class TestShift(TestCase):
    def setUp(self):
        user = create_user()
        self.shift_code = models.ShiftCode.objects.create(
            code='A1',
            sb_user=user,
            role='p',
            monday_start='01:00',
            monday_duration='1.1',
            tuesday_start='02:00',
            tuesday_duration='2.2',
            wednesday_start='03:00',
            wednesday_duration='3.3',
            thursday_start='04:00',
            thursday_duration='4.4',
            friday_start='05:00',
            friday_duration='5.5',
            saturday_start='06:00',
            saturday_duration='6.6',
            sunday_start='07:00',
            sunday_duration='7.7',
            stat_start='08:00',
            stat_duration='8.8',
        )
        self.shift = models.Shift.objects.create(
            sb_user=user,
            date='2018-01-01',
            shift_code=self.shift_code,
            text_shift_code='A1',
        )

    def test_labels(self):
        self.assertEqual(
            self.shift._meta.get_field('sb_user').verbose_name,
            'SB user',
        )
        self.assertEqual(
            self.shift._meta.get_field('date').verbose_name,
            'date',
        )
        self.assertEqual(
            self.shift._meta.get_field('shift_code').verbose_name,
            'shift code',
        )
        self.assertEqual(
            self.shift._meta.get_field('text_shift_code').verbose_name,
            'text shift code',
        )

    def test_max_lengths(self):
        self.assertEqual(
            self.shift._meta.get_field('text_shift_code').max_length,
            20
        )

    def test_str(self):
        self.assertEqual(
            str(self.shift),
            '2018-01-01 - Pharmacist - Regular User - A1'
        )

class TestMissingShiftCode(TestCase):
    def setUp(self):
        self.missing = models.MissingShiftCode.objects.create(
            code='A2',
            role='p',
        )

    def test_labels(self):
        self.assertEqual(
            self.missing._meta.get_field('code').verbose_name,
            'code',
        )
        self.assertEqual(
            self.missing._meta.get_field('role').verbose_name,
            'role',
        )

    def test_max_lengths(self):
        self.assertEqual(
            self.missing._meta.get_field('code').max_length,
            20
        )
        self.assertEqual(
            self.missing._meta.get_field('role').max_length,
            1
        )

    def test_role_choices(self):
        choices = self.missing._meta.get_field('role').choices

        self.assertTrue(('a', 'Pharmacy Assistant') in choices)
        self.assertTrue(('p', 'Pharmacist') in choices)
        self.assertTrue(('t', 'Pharmacy Technician') in choices)

    def test_str(self):
        self.assertEqual(
            str(self.missing),
            'A2 - p'
        )
