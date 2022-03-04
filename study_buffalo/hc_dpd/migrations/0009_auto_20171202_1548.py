# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0008_auto_20171127_0757'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ActiveIngredients',
            new_name='ActiveIngredient',
        ),
        migrations.RenameModel(
            old_name='Companies',
            new_name='Company',
        ),
        migrations.RenameModel(
            old_name='InactiveProducts',
            new_name='InactiveProduct',
        ),
    ]
