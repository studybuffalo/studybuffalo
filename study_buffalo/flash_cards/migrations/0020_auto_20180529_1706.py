# Generated by Django 2.0.3 on 2018-05-29 23:06

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0019_auto_20180529_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalreference',
            name='reference_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='reference UUID'),
        ),
        migrations.AddField(
            model_name='reference',
            name='reference_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='reference UUID'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='references', to='flash_cards.Card'),
        ),
    ]
