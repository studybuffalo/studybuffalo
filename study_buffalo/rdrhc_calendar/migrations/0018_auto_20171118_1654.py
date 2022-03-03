# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0017_auto_20171027_1851'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='missingshiftcode',
            options={
                'permissions': (('can_add_default_codes', 'Can add new default codes to the ShiftCode database'),),
            },
        ),
    ]
