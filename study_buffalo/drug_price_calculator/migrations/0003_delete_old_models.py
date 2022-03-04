# pylint: disable=missing-module-docstring, missing-class-docstring
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drug_price_calculator', '0002_increase_coverage_field_length'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ATC',
        ),
        migrations.DeleteModel(
            name='ATCDescriptions',
        ),
        migrations.DeleteModel(
            name='Coverage',
        ),
        migrations.DeleteModel(
            name='ExtraInformation',
        ),
        migrations.DeleteModel(
            name='PendPTC',
        ),
        migrations.DeleteModel(
            name='Price',
        ),
        migrations.DeleteModel(
            name='PTC',
        ),
        migrations.DeleteModel(
            name='SpecialAuthorization',
        ),
        migrations.DeleteModel(
            name='SubsPTC',
        ),
    ]
