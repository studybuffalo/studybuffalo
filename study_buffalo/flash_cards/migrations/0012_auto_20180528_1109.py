# Generated by Django 2.0.3 on 2018-05-28 17:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0011_auto_20180528_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='answer_freeform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='answer_freeform', to='flash_cards.PartContainer', verbose_name='freeform answer'),
        ),
        migrations.AlterField(
            model_name='card',
            name='answer_matching',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='flash_cards.MatchingAnswer', verbose_name='matcing answer'),
        ),
        migrations.AlterField(
            model_name='card',
            name='answer_multiple_choice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='flash_cards.MultipleChoiceContainer', verbose_name='multiple choice answer'),
        ),
        migrations.AlterField(
            model_name='card',
            name='card_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='card UUID'),
        ),
        migrations.AlterField(
            model_name='historicalcard',
            name='card_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='card UUID'),
        ),
    ]
