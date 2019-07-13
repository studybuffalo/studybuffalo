# Generated by Django 2.2.3 on 2019-07-13 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drug_price_calculator', '0008_renaming_bsrf'),
    ]

    operations = [
        migrations.AddField(
            model_name='atc',
            name='atc_5',
            field=models.CharField(max_length=7, null=True, verbose_name='ATC level 5 code'),
        ),
        migrations.AddField(
            model_name='atc',
            name='atc_5_text',
            field=models.CharField(max_length=200, null=True, verbose_name='ATC level 5 description'),
        ),
    ]
