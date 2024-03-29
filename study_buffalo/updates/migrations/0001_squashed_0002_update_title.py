# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('updates', '0001_initial'), ('updates', '0002_update_title')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Update',
            fields=[
                (
                    'id',
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                (
                    'background',
                    models.ImageField(
                        blank=True,
                        help_text='Optional background image',
                        null=True,
                        upload_to='home/update/',
                    ),
                ),
                (
                    'icon',
                    models.ImageField(help_text='Image for the update icon', upload_to='home/update/'),
                ),
                (
                    'html',
                    models.TextField(blank=True, help_text='Any HTML to accompany the update'),
                ),
                (
                    'start_date',
                    models.DateField(
                        default=django.utils.timezone.now,
                        help_text='Date to start displaying the update',
                    ),
                ),
                (
                    'end_date',
                    models.DateField(
                        blank=True,
                        help_text='Date to stop displaying the update (leave blank for no end date)',
                        null=True,
                    ),
                ),
                (
                    'priority',
                    models.SmallIntegerField(
                        default=1,
                        help_text='The priority order to show the slide',
                    ),
                ),
                (
                    'title',
                    models.CharField(default='title', max_length=256),
                ),
            ],
            options={
                'verbose_name': 'Update',
                'verbose_name_plural': 'Updates',
                'ordering': ['priority', 'start_date'],
            },
        ),
    ]
