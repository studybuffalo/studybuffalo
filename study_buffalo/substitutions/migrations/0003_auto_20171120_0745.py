# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitutions', '0002_auto_20171119_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelfields',
            name='field_type',
            field=models.CharField(
                choices=[('o', 'Original'), ('s', 'Substitution')],
                default='s',
                help_text='Whether this is an original or substitution field',
                max_length=1,
            ),
        ),
        migrations.AddField(
            model_name='modelfields',
            name='google_check',
            field=models.BooleanField(
                default=False,
                help_text='Whether to provide a online search button with the field entry',
            ),
        ),
        migrations.AlterField(
            model_name='modelfields',
            name='dictionary_check',
            field=models.BooleanField(
                default=False,
                help_text='Whether to search for field value in the dictionary',
            ),
        ),
    ]
