# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [
        ('study', '0001_initial'),
        ('study', '0002_auto_20170828_2057'),
        ('study', '0003_remove_guide_guide_type'),
    ]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bounty',
            fields=[
                (
                    'id',
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                (
                    'bounty_status',
                    models.CharField(
                        choices=[('o', 'Open'), ('c', 'Completed')],
                        default='o',
                        help_text='The status of the bounty',
                        max_length=1,
                    ),
                ),
                (
                    'bounty_amount',
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        help_text='The amount to be awarded on completion of the bounty',
                        max_digits=6,
                    ),
                ),
                (
                    'bounty_details',
                    models.TextField(help_text='The details of the bounty; supports HTML'),
                ),
            ],
            options={
                'ordering': ['study_guide', 'bounty_status'],
            },
        ),
        migrations.CreateModel(
            name='BountyAssignment',
            fields=[
                (
                    'id',
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                (
                    'assignment_status',
                    models.CharField(
                        choices=[('i', 'In progress'), ('r', 'Rewarded')],
                        help_text='The current status of the user\'s work on the bounty',
                        max_length=1,
                    ),
                ),
                (
                    'proportion',
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        help_text='The proprtion of the bounty award the user received',
                        max_digits=3,
                    ),
                ),
                (
                    'assigned_user',
                    models.ForeignKey(
                        help_text='The user assigned to this bounty',
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'bounty',
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.Bounty'),
                ),
            ],
            options={
                'ordering': ['bounty', 'proportion', 'assigned_user'],
            },
        ),
        migrations.CreateModel(
            name='DocumentGuide',
            fields=[
                (
                    'id',
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                (
                    'document',
                    models.FileField(
                        help_text='The study guide file to upload (PDF preferred)',
                        upload_to='study_guides',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Guide',
            fields=[
                (
                    'id',
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                (
                    'title',
                    models.CharField(help_text='The title of the study guide', max_length=100),
                ),
                (
                    'short_description',
                    models.CharField(help_text='A short description of the study guide', max_length=256),
                ),
                (
                    'long_description',
                    models.TextField(
                        blank=True,
                        help_text='A longer description of the study guide; supports HTML',
                        null=True,
                    ),
                ),
                (
                    'date_original',
                    models.DateField(help_text='The date the first version was released'),
                ),
                (
                    'last_update',
                    models.DateField(help_text='The date of the last update'),
                ),
                (
                    'guide_type',
                    models.CharField(choices=[('d', 'Document'), ('h', 'HTML')], default='d', max_length=1),
                ),
                (
                    'permissions',
                    models.CharField(
                        blank=True,
                        choices=[('dsm', 'DSM Study Guide')],
                        help_text='If the study guide has any special permissions to access it',
                        max_length=3,
                        null=True,
                    ),
                ),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='HTMLGuide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('html', models.TextField(help_text='The HTML content to display the guide')),
                ('study_guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.Guide')),
            ],
        ),
        migrations.AddField(
            model_name='documentguide',
            name='study_guide',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.Guide'),
        ),
        migrations.AddField(
            model_name='bounty',
            name='study_guide',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.Guide'),
        ),
        migrations.RemoveField(
            model_name='guide',
            name='guide_type',
        ),
    ]
