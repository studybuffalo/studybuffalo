# Generated by Django 2.2.3 on 2019-07-14 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drug_price_calculator', '0010_adding_blank_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialauthorization',
            name='pdf_title',
            field=models.CharField(help_text='The tile of the PDF', max_length=200),
        ),
    ]