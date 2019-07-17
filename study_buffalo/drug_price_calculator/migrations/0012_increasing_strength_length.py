from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('drug_price_calculator', '0011_increasing_pdf_title_max_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug',
            name='strength',
            field=models.CharField(
                blank=True,
                help_text='The strength(s) of the medications',
                max_length=225,
                null=True
            ),
        ),
    ]
