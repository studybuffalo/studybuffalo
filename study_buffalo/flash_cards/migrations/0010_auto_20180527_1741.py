# Generated by Django 2.0.3 on 2018-05-27 23:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0009_auto_20180527_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='flash_cards.PartContainer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalcard',
            name='question',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='flash_cards.PartContainer'),
        ),
        migrations.AlterField(
            model_name='card',
            name='answer_freeform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='answer_freeform', to='flash_cards.PartContainer'),
        ),
    ]
