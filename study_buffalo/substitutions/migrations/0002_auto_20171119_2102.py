# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitutions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apps',
            options={'verbose_name': 'Application', 'verbose_name_plural': 'Applications'},
        ),
        migrations.AlterField(
            model_name='apps',
            name='app_name',
            field=models.CharField(help_text='The name of the Django App to include', max_length=50),
        ),
        migrations.AlterField(
            model_name='apps',
            name='model_pending',
            field=models.CharField(help_text='The model name containing the pending substitutions', max_length=50),
        ),
        migrations.AlterField(
            model_name='apps',
            name='model_sub',
            field=models.CharField(
                help_text='The model name where the verified substitutions should be added to',
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name='modelfields',
            name='dictionary_check',
            field=models.BooleanField(
                default=False,
                help_text='Whether to add a online search button to confirm spelling',
            ),
        ),
        migrations.AlterField(
            model_name='modelfields',
            name='field_name',
            field=models.CharField(help_text='A field name from the model to include', max_length=50),
        ),
    ]
