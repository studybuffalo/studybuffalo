# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0006_auto_20171120_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='route_of_administration',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='subrouteofadministration',
            name='original',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='subrouteofadministration',
            name='substitution',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='subrouteofadministrationpend',
            name='original',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='subrouteofadministrationpend',
            name='substitution',
            field=models.CharField(max_length=50),
        ),
    ]
