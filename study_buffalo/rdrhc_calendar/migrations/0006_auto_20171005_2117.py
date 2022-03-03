# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0005_auto_20171005_1806'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shiftcode',
            unique_together=set([('code', 'user', 'role')]),
        ),
    ]
