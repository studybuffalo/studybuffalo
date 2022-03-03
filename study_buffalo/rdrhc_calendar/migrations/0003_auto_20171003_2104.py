# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0002_auto_20171003_2051'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StatHolidays',
            new_name='StatHoliday',
        ),
        migrations.AlterModelOptions(
            name='calendaruser',
            options={'verbose_name': 'RDRHC Calendar User', 'verbose_name_plural': 'RDRHC Calendar Users'},
        ),
        migrations.AlterModelOptions(
            name='shiftcode',
            options={'verbose_name': 'Shift Code', 'verbose_name_plural': 'Shift Codes'},
        ),
        migrations.AlterModelOptions(
            name='statholiday',
            options={'verbose_name': 'Stat Holiday', 'verbose_name_plural': 'Stat Holidays\''},
        ),
    ]
