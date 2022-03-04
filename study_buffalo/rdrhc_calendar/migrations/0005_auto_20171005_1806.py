# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0004_auto_20171005_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiftcode',
            name='code',
            field=models.CharField(help_text='The shift code used in the Excel schedule', max_length=20),
        ),
        migrations.AlterField(
            model_name='shiftcode',
            name='user',
            field=models.ForeignKey(
                blank=True,
                help_text='Which user this shift code applies to (leave blank for a default entry)',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='rdrhc_calendar.CalendarUser',
            ),
        ),
    ]
