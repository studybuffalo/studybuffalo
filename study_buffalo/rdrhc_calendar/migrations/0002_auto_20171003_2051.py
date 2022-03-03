# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiftcode',
            name='role',
            field=models.CharField(
                choices=[('a', 'Pharmacy Assistant'), ('p', 'Pharmacist'), ('t', 'Pharmacy Technician')],
                default='p',
                help_text='The role/profession this code applies to',
                max_length=1,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shiftcode',
            name='user',
            field=models.ForeignKey(
                blank=True,
                help_text='Which user this shift code applies to (leave blank for a default entry',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='rdrhc_calendar.CalendarUser',
            ),
        ),
    ]
