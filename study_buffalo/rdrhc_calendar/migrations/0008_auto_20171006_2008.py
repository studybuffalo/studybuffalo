# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0007_auto_20171005_2130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shift',
            old_name='name',
            new_name='user',
        ),
    ]
