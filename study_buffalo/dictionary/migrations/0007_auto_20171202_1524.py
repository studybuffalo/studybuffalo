# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0006_auto_20171202_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='dictionaryclass',
            name='class_verbose_name',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dictionarytype',
            name='dictionary_verbose_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
