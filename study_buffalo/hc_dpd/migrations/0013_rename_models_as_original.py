# pylint: disable=missing-module-docstring, missing-class-docstring
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0012_align_with_hc_20220301_2'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ActiveIngredient',
            new_name='OriginalActiveIngredient',
        ),
        migrations.RenameModel(
            old_name='Company',
            new_name='OriginalCompany',
        ),
        migrations.RenameModel(
            old_name='DrugProduct',
            new_name='OriginalDrugProduct',
        ),
        migrations.RenameModel(
            old_name='Form',
            new_name='OriginalForm',
        ),
        migrations.RenameModel(
            old_name='InactiveProduct',
            new_name='OriginalInactiveProduct',
        ),
        migrations.RenameModel(
            old_name='Packaging',
            new_name='OriginalPackaging',
        ),
        migrations.RenameModel(
            old_name='PharmaceuticalStandard',
            new_name='OriginalPharmaceuticalStandard',
        ),
        migrations.RenameModel(
            old_name='Route',
            new_name='OriginalRoute',
        ),
        migrations.RenameModel(
            old_name='Schedule',
            new_name='OriginalSchedule',
        ),
        migrations.RenameModel(
            old_name='Status',
            new_name='OriginalStatus',
        ),
        migrations.RenameModel(
            old_name='TherapeuticClass',
            new_name='OriginalTherapeuticClass',
        ),
        migrations.RenameModel(
            old_name='VeterinarySpecies',
            new_name='OriginalVeterinarySpecies',
        ),
    ]
