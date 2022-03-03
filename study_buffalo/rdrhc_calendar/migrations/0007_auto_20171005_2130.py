# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0006_auto_20171005_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiftcode',
            name='friday_duration',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=15.0,
                help_text='The duration of the shift in hours (defaults to 15 hours)',
                max_digits=4,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='shiftcode',
            name='monday_duration',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=15.0,
                help_text='The duration of the shift in hours (defaults to 15 hours)',
                max_digits=4,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='shiftcode',
            name='saturday_duration',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=15.0,
                help_text='The duration of the shift in hours (defaults to 15 hours)',
                max_digits=4,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='shiftcode',
            name='stat_duration',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=15.0,
                help_text='The duration of the shift in hours (defaults to 15 hours)',
                max_digits=4,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='shiftcode',
            name='sunday_duration',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=15.0,
                help_text='The duration of the shift in hours (defaults to 15 hours)',
                max_digits=4,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='shiftcode',
            name='thursday_duration',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=15.0,
                help_text='The duration of the shift in hours (defaults to 15 hours)',
                max_digits=4,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='shiftcode',
            name='tuesday_duration',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=15.0,
                help_text='The duration of the shift in hours (defaults to 15 hours)',
                max_digits=4,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='shiftcode',
            name='wednesday_duration',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=15.0,
                help_text='The duration of the shift in hours (defaults to 15 hours)',
                max_digits=4,
                null=True,
            ),
        ),
    ]
