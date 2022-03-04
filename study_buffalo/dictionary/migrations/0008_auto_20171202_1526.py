# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0007_auto_20171202_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictionaryclass',
            name='class_verbose_name',
            field=models.CharField(max_length=50),
        ),
    ]
