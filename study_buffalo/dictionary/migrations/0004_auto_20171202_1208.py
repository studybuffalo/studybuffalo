# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-02 19:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0003_auto_20171121_1911'),
    ]

    operations = [
        migrations.CreateModel(
            name='DictionaryClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='wordpending',
            name='original_words',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='excludedword',
            name='dictionary_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dictionary.DictionaryClass'),
        ),
        migrations.AddField(
            model_name='word',
            name='dictionary_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dictionary.DictionaryClass'),
        ),
        migrations.AddField(
            model_name='wordpending',
            name='dictionary_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dictionary.DictionaryClass'),
        ),
    ]
