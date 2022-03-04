# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0015_auto_20171016_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendaruser',
            name='email',
        ),
    ]
