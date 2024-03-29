# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0016_remove_calendaruser_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='MissingShiftCode',
            fields=[
                (
                    'id',
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                (
                    'code',
                    models.CharField(help_text='The shift code used in the Excel schedule', max_length=20),
                ),
                (
                    'role',
                    models.CharField(
                        choices=[('a', 'Pharmacy Assistant'), ('p', 'Pharmacist'), ('t', 'Pharmacy Technician')],
                        help_text='The role/profession this code applies to',
                        max_length=1,
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='missingshiftcode',
            unique_together=set([('code', 'role')]),
        ),
    ]
