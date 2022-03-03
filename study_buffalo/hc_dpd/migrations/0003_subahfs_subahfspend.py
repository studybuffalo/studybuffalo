# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0002_auto_20171120_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubAHFS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=80, unique=True)),
                ('substitution', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='SubAHFSPend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=80, unique=True)),
                ('substitution', models.CharField(max_length=80)),
            ],
        ),
    ]
