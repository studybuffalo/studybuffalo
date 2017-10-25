# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-25 23:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_manager', '0011_auto_20171023_1939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appdata',
            name='flag_end',
        ),
        migrations.RemoveField(
            model_name='appdata',
            name='flag_start',
        ),
        migrations.AddField(
            model_name='appdata',
            name='monitor_start',
            field=models.BooleanField(default=False, help_text='Whether to notify the user or not if there are no new logentries when the log monitor checks at the specified time'),
        ),
    ]
