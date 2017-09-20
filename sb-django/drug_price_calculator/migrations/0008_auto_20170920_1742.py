# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-20 23:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drug_price_calculator', '0007_auto_20170920_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendgeneric',
            name='correction',
            field=models.CharField(max_length=450),
        ),
        migrations.AlterField(
            model_name='pendgeneric',
            name='original',
            field=models.CharField(max_length=450, unique=True),
        ),
        migrations.AlterField(
            model_name='subsgeneric',
            name='correction',
            field=models.CharField(max_length=450),
        ),
        migrations.AlterField(
            model_name='subsgeneric',
            name='original',
            field=models.CharField(max_length=450, unique=True),
        ),
    ]
