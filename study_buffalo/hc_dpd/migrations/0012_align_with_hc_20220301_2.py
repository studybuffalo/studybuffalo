# pylint: disable=missing-module-docstring, missing-class-docstring
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0011_align_with_hc_20220301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_name',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='street_name',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
