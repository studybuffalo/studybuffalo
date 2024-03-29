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
            name='Apps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=50)),
                ('model_pending', models.CharField(max_length=50)),
                ('model_sub', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ModelFields',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=50)),
                ('dictionary_check', models.BooleanField(default=False)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='substitutions.Apps')),
            ],
        ),
    ]
