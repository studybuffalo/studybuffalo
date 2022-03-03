# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0014_auto_20171016_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='shift_code',
            field=models.ForeignKey(
                blank=True,
                help_text='The shift code for this shift',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='rdrhc_calendar.ShiftCode',
            ),
        ),
    ]
