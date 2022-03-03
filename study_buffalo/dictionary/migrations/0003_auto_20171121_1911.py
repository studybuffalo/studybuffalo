# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_auto_20171121_1812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='excludedwordpending',
            name='dictionary_type',
        ),
        migrations.RemoveField(
            model_name='excludedwordpending',
            name='language',
        ),
        migrations.DeleteModel(
            name='ExcludedWordPending',
        ),
    ]
