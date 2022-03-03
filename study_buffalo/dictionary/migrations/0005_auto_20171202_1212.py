# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0004_auto_20171202_1208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitoredfield',
            name='dictionary_type',
        ),
        migrations.RemoveField(
            model_name='monitoredfield',
            name='language',
        ),
        migrations.RemoveField(
            model_name='monitoredfield',
            name='monitored_model',
        ),
        migrations.RemoveField(
            model_name='monitoredmodel',
            name='monitored_application',
        ),
        migrations.AlterModelOptions(
            name='wordpending',
            options={
                'permissions': (('can_view', 'Can view the dictionary review application'),),
                'verbose_name': 'Word (Pending)',
                'verbose_name_plural': 'Words (Pending)',
            },
        ),
        migrations.DeleteModel(
            name='MonitoredApplication',
        ),
        migrations.DeleteModel(
            name='MonitoredField',
        ),
        migrations.DeleteModel(
            name='MonitoredModel',
        ),
    ]
