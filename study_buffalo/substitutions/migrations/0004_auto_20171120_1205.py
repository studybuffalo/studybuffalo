# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('substitutions', '0003_auto_20171120_0745'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apps',
            options={
                'permissions': (('can_view', 'Can view the substitution application'),),
                'verbose_name': 'Application',
                'verbose_name_plural': 'Applications',
            },
        ),
    ]
