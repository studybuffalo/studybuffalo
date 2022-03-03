# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0004_auto_20171120_1359'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SubUPC',
        ),
        migrations.DeleteModel(
            name='SubUPCPend',
        ),
        migrations.AlterModelOptions(
            name='subproductcategorization',
            options={
                'verbose_name': 'Substitution - Product Categorization',
                'verbose_name_plural': 'Substitutions - Product Categorization',
            },
        ),
        migrations.AlterModelOptions(
            name='subsuitenumberpend',
            options={
                'verbose_name': 'Substitution - Suite Number (Pending)',
                'verbose_name_plural': 'Substitutions - Suite Number (Pending)',
            },
        ),
    ]
