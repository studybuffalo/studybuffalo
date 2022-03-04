# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SubAHFS',
        ),
        migrations.DeleteModel(
            name='SubAHFSPend',
        ),
    ]
