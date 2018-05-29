# Generated by Django 2.0.3 on 2018-05-29 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0016_auto_20180528_2059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaluserstats',
            name='number_sets',
        ),
        migrations.RemoveField(
            model_name='userstats',
            name='number_sets',
        ),
        migrations.AddField(
            model_name='historicaluserstats',
            name='number_decks',
            field=models.IntegerField(default=0, verbose_name='decks completed'),
        ),
        migrations.AddField(
            model_name='userstats',
            name='number_decks',
            field=models.IntegerField(default=0, verbose_name='decks completed'),
        ),
        migrations.AlterField(
            model_name='historicaluserstats',
            name='number_questions',
            field=models.IntegerField(default=0, verbose_name='questions completed'),
        ),
        migrations.AlterField(
            model_name='userstats',
            name='number_questions',
            field=models.IntegerField(default=0, verbose_name='questions completed'),
        ),
    ]
