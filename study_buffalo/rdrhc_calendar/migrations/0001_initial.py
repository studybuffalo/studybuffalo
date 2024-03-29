# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarUser',
            fields=[
                (
                    'id',
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                (
                    'name',
                    models.CharField(help_text='The name of the user', max_length=25),
                ),
                (
                    'schedule_name',
                    models.CharField(help_text='The name of the user on the Excel schedule', max_length=25),
                ),
                (
                    'calendar_name',
                    models.CharField(help_text='The name of calendar (the .ics file)', max_length=50),
                ),
                (
                    'email',
                    models.EmailField(
                        help_text='The email to use for contacting the user with their calendar',
                        max_length=254,
                    ),
                ),
                (
                    'role',
                    models.CharField(
                        choices=[('a', 'Pharmacy Assistant'), ('p', 'Pharmacist'), ('t', 'Pharmacy Technician')],
                        help_text='The role/profession of the user',
                        max_length=1,
                    ),
                ),
                (
                    'first_email_sent',
                    models.BooleanField(default=False, help_text='Whether the welcome email has been sent or not'),
                ),
                (
                    'full_day',
                    models.BooleanField(
                        default=False,
                        help_text='Whether the .ics calender should show shifts as full day events or not',
                    ),
                ),
                (
                    'reminder',
                    models.IntegerField(
                        blank=True,
                        help_text=(
                            'How much time before the shift starts (in '
                            'minutes) to provide a reminder (leave blank '
                            'for no reminder)'
                        ),
                        null=True,
                    ),
                ),
                (
                    'sb_user',
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                (
                    'id',
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                (
                    'date',
                    models.DateField(help_text='The date of the shift'),
                ),
                (
                    'name',
                    models.ForeignKey(
                        help_text='The user this shit applies to',
                        on_delete=django.db.models.deletion.CASCADE,
                        to='rdrhc_calendar.CalendarUser',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='ShiftCode',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'code',
                    models.CharField(
                        help_text='The shift code used in the Excel schedule',
                        max_length=10,
                    ),
                ),
                (
                    'monday_start',
                    models.TimeField(
                        blank=True,
                        default=datetime.time(7, 0),
                        help_text='The start time of the shift (leave blank if there should be no shift at this time)',
                        null=True,
                    ),
                ),
                (
                    'monday_duration',
                    models.DecimalField(
                        decimal_places=2,
                        default=15.0,
                        help_text='The duration of the shift in hours (defaults to 15 hours)',
                        max_digits=4,
                    ),
                ),
                (
                    'tuesday_start',
                    models.TimeField(
                        blank=True,
                        default=datetime.time(7, 0),
                        help_text='The start time of the shift (leave blank if there should be no shift at this time)',
                        null=True,
                    ),
                ),
                (
                    'tuesday_duration',
                    models.DecimalField(
                        decimal_places=2,
                        default=15.0,
                        help_text='The duration of the shift in hours (defaults to 15 hours)',
                        max_digits=4,
                    ),
                ),
                (
                    'wednesday_start',
                    models.TimeField(
                        blank=True,
                        default=datetime.time(7, 0),
                        help_text='The start time of the shift (leave blank if there should be no shift at this time)',
                        null=True,
                    ),
                ),
                (
                    'wednesday_duration',
                    models.DecimalField(
                        decimal_places=2,
                        default=15.0,
                        help_text='The duration of the shift in hours (defaults to 15 hours)',
                        max_digits=4,
                    ),
                ),
                (
                    'thursday_start',
                    models.TimeField(
                        blank=True,
                        default=datetime.time(7, 0),
                        help_text='The start time of the shift (leave blank if there should be no shift at this time)',
                        null=True,
                    ),
                ),
                (
                    'thursday_duration',
                    models.DecimalField(
                        decimal_places=2,
                        default=15.0,
                        help_text='The duration of the shift in hours (defaults to 15 hours)',
                        max_digits=4,
                    ),
                ),
                (
                    'friday_start',
                    models.TimeField(
                        blank=True,
                        default=datetime.time(7, 0),
                        help_text='The start time of the shift (leave blank if there should be no shift at this time)',
                        null=True,
                    ),
                ),
                (
                    'friday_duration',
                    models.DecimalField(
                        decimal_places=2,
                        default=15.0,
                        help_text='The duration of the shift in hours (defaults to 15 hours)',
                        max_digits=4,
                    ),
                ),
                (
                    'saturday_start',
                    models.TimeField(
                        blank=True, default=datetime.time(7, 0),
                        help_text='The start time of the shift (leave blank if there should be no shift at this time)',
                        null=True,
                    ),
                ),
                (
                    'saturday_duration',
                    models.DecimalField(
                        decimal_places=2,
                        default=15.0,
                        help_text='The duration of the shift in hours (defaults to 15 hours)',
                        max_digits=4,
                    ),
                ),
                (
                    'sunday_start',
                    models.TimeField(
                        blank=True,
                        default=datetime.time(7, 0),
                        help_text='The start time of the shift (leave blank if there should be no shift at this time)',
                        null=True,
                    ),
                ),
                (
                    'sunday_duration',
                    models.DecimalField(
                        decimal_places=2,
                        default=15.0,
                        help_text='The duration of the shift in hours (defaults to 15 hours)',
                        max_digits=4,
                    ),
                ),
                (
                    'stat_start',
                    models.TimeField(
                        blank=True,
                        default=datetime.time(7, 0),
                        help_text='The start time of the shift (leave blank if there should be no shift at this time)',
                        null=True,
                    ),
                ),
                (
                    'stat_duration',
                    models.DecimalField(
                        decimal_places=2,
                        default=15.0,
                        help_text='The duration of the shift in hours (defaults to 15 hours)',
                        max_digits=4,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='StatHolidays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='shift',
            name='shift_code',
            field=models.ForeignKey(
                help_text='The shift code for this shift',
                on_delete=django.db.models.deletion.PROTECT,
                to='rdrhc_calendar.ShiftCode',
            ),
        ),
    ]
