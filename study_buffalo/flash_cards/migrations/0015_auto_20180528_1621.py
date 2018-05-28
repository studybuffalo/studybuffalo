# Generated by Django 2.0.3 on 2018-05-28 22:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0014_auto_20180528_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='deck_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='deck UUID'),
        ),
        migrations.AlterField(
            model_name='historicaldeck',
            name='deck_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='deck UUID'),
        ),
    ]
