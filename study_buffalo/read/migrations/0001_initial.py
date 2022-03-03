# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentPublication',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                (
                    'document',
                    models.FileField(
                        help_text='The publicationfile to upload (PDF preferred)', upload_to='publications',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='HTMLPublication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('html', models.TextField(help_text='The HTML content to display the publication')),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='The title of the study guide', max_length=100)),
                ('description', models.CharField(help_text='A short description of the study guide', max_length=256)),
                ('date_published', models.DateField(help_text='The date the first version was released')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.AddField(
            model_name='htmlpublication',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='read.Publication'),
        ),
        migrations.AddField(
            model_name='documentpublication',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='read.Publication'),
        ),
    ]
