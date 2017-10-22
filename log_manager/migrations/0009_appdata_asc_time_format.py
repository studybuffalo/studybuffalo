# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-22 18:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_manager', '0008_auto_20171022_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='appdata',
            name='asc_time_format',
            field=models.CharField(default='Y-m-d H:M:S,f', help_text='The format of the asc_time field', max_length=50),
            preserve_default=False,
        ),
    ]
