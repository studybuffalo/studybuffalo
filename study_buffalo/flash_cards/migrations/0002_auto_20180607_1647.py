# Generated by Django 2.0.3 on 2018-06-07 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='description',
            field=models.TextField(default=' ', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicaldeck',
            name='description',
            field=models.TextField(default=' ', max_length=500),
            preserve_default=False,
        ),
    ]
