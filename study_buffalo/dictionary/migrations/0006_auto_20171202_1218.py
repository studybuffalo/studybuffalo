# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0005_auto_20171202_1212'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dictionaryclass',
            options={'verbose_name': 'Dictionary class', 'verbose_name_plural': 'Dictionary classes'},
        ),
    ]
