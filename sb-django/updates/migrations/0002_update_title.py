# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-24 19:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='title',
            field=models.CharField(default='title', max_length=256),
            preserve_default=False,
        ),
    ]
