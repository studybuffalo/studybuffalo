# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0011_auto_20171016_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='user',
            field=models.ForeignKey(
                help_text='The user this shit applies to',
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
