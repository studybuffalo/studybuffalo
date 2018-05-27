# Generated by Django 2.0.3 on 2018-05-27 23:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0006_auto_20180527_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='historicalcard',
            name='card_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
