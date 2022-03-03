# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0005_auto_20171120_1436'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SubCompanyType',
        ),
        migrations.DeleteModel(
            name='SubCompanyTypePend',
        ),
    ]
