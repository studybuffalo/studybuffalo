# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

import uuid

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [
        ('play', '0001_initial'),
        ('play', '0002_auto_20170827_2214'),
        ('play', '0003_auto_20170827_2214'),
        ('play', '0004_auto_20170827_2221'),
        ('play', '0005_auto_20170828_0732'),
        ('play', '0006_auto_20170828_0924'),
        ('play', '0007_auto_20170828_1014'),
        ('play', '0008_auto_20170828_1416'),
    ]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(help_text='The name of the category', max_length=100)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='PlayAudio',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Unqiue ID for this item',
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'title',
                    models.CharField(help_text='Title to display above the audio player', max_length=256, null=True),
                ),
                (
                    'type',
                    models.CharField(default='a', editable=False, help_text='The file type of the item', max_length=1),
                ),
                (
                    'location',
                    models.FileField(help_text='The uploaded audio content', upload_to='play/audio/'),
                ),
                (
                    'description',
                    models.TextField(help_text='Any additional text to display below the image', null=True),
                ),
                (
                    'ordering',
                    models.PositiveSmallIntegerField(default=1),
                ),
            ],
            options={
                'verbose_name': 'Audio',
                'verbose_name_plural': 'Audio',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='PlayImage',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='Unqiue ID for this item',
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'title',
                    models.CharField(help_text='Title to display above the image', max_length=256, null=True),
                ),
                (
                    'type',
                    models.CharField(
                        default='i',
                        editable=False,
                        help_text='The file type of the item',
                        max_length=1,
                    ),
                ),
                (
                    'location',
                    models.ImageField(
                        help_text='The uploaded image (high quality)',
                        upload_to='play/images/original/',
                    ),
                ),
                (
                    'alt_text',
                    models.CharField(
                        help_text='Text to show on cursor hover over the item',
                        max_length=256,
                        null=True,
                    ),
                ),
                (
                    'description',
                    models.TextField(help_text='Any additional text to display below the image', null=True),
                ),
                (
                    'ordering',
                    models.PositiveSmallIntegerField(default=1),
                ),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='PlayPage',
            fields=[
                (
                    'id',
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                (
                    'title',
                    models.CharField(help_text='Title for the page', max_length=256),
                ),
                (
                    'date',
                    models.DateField(default=django.utils.timezone.now, help_text='Date the play item was released'),
                ),
                (
                    'category',
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='play.Category'),
                ),
                (
                    'release_date',
                    models.DateTimeField(default=django.utils.timezone.now, help_text='Date to release this page on'),
                ),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
                'ordering': ['date', 'title'],
            },
        ),
        migrations.AddField(
            model_name='playimage',
            name='page',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='play.PlayPage',
            ),
        ),
        migrations.AddField(
            model_name='playaudio',
            name='page',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='play.PlayPage',
            ),
        ),
        migrations.RenameField(
            model_name='playimage',
            old_name='location',
            new_name='original_image',
        ),
        migrations.AddField(
            model_name='playimage',
            name='resized_image',
            field=models.ImageField(default='', editable=False, upload_to='play/images/resized/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playaudio',
            name='description',
            field=models.TextField(blank=True, default='', help_text='Any additional text to display below the image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playaudio',
            name='title',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Title to display above the audio player',
                max_length=256,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playimage',
            name='alt_text',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Text to show on cursor hover over the item',
                max_length=256,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playimage',
            name='description',
            field=models.TextField(blank=True, default='', help_text='Any additional text to display below the image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playimage',
            name='title',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Title to display above the image',
                max_length=256,
            ),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='playaudio',
            old_name='location',
            new_name='audio',
        ),
        migrations.AlterModelOptions(
            name='playimage',
            options={'ordering': ['ordering', 'title'], 'verbose_name': 'Image', 'verbose_name_plural': 'Images'},
        ),
    ]
