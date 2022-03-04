# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0010_auto_20171016_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendaruser',
            name='calendar_name',
            field=models.CharField(help_text='The name of your calendar file', max_length=50, unique=True),
        ),
    ]
