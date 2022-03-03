# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0009_auto_20171006_2100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calendaruser',
            options={
                'permissions': (('can_view', 'Can view the RDRHC Calendar settings view'),),
                'verbose_name': 'RDRHC Calendar User',
                'verbose_name_plural': 'RDRHC Calendar Users',
            },
        ),
        migrations.AlterField(
            model_name='calendaruser',
            name='sb_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
