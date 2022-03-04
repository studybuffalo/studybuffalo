# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0001_squashed_0002_update_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update',
            name='title',
            field=models.CharField(max_length=256),
        ),
    ]
