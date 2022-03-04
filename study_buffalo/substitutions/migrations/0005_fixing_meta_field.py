# pylint: disable=missing-module-docstring, missing-class-docstring
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('substitutions', '0004_auto_20171120_1205'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='modelfields',
            options={'verbose_name': 'Model Field', 'verbose_name_plural': 'Model Fields'},
        ),
    ]
