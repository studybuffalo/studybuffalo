# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-18 23:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0017_auto_20171027_1851'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='missingshiftcode',
            options={'permissions': (('can_add_default_codes', 'Can add new default codes to the ShiftCode database'),)},
        ),
    ]
