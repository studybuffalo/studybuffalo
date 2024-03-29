# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0008_auto_20171006_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='text_shift_code',
            field=models.CharField(default='', help_text='Text representation of the shift code', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shift',
            name='shift_code',
            field=models.ForeignKey(
                blank=True,
                help_text='The shift code for this shift',
                null=True, on_delete=django.db.models.deletion.PROTECT,
                to='rdrhc_calendar.ShiftCode',
            ),
        ),
    ]
