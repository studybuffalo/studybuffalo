# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-02 22:26
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
