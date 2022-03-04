# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0007_auto_20171120_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companies',
            name='street_name',
            field=models.CharField(blank=True, max_length=90, null=True),
        ),
        migrations.AlterField(
            model_name='substreetname',
            name='original',
            field=models.CharField(max_length=90, unique=True),
        ),
        migrations.AlterField(
            model_name='substreetname',
            name='substitution',
            field=models.CharField(max_length=90),
        ),
        migrations.AlterField(
            model_name='substreetnamepend',
            name='original',
            field=models.CharField(max_length=90, unique=True),
        ),
        migrations.AlterField(
            model_name='substreetnamepend',
            name='substitution',
            field=models.CharField(max_length=90),
        ),
    ]
