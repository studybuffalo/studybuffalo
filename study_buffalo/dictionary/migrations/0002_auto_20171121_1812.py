# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='excludedwordpending',
            options={'verbose_name': 'Excluded Word (Pending)', 'verbose_name_plural': 'Excluded Words (Pending)'},
        ),
        migrations.AlterModelOptions(
            name='monitoredapplication',
            options={'permissions': (('can_view', 'Can view the dictionary review application'),)},
        ),
        migrations.AlterModelOptions(
            name='wordpending',
            options={'verbose_name': 'Word (Pending)', 'verbose_name_plural': 'Words (Pending)'},
        ),
    ]
