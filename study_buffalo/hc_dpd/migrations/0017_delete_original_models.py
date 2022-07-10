# pylint: disable=missing-module-docstring, missing-class-docstring, line-too-long
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('hc_dpd', '0016_delete_ahfs_add_meta'),
    ]

    operations = [
        migrations.DeleteModel(name='OriginalActiveIngredient'),
        migrations.DeleteModel(name='OriginalBiosimilar'),
        migrations.DeleteModel(name='OriginalCompany'),
        migrations.DeleteModel(name='OriginalDrugProduct'),
        migrations.DeleteModel(name='OriginalForm'),
        migrations.DeleteModel(name='OriginalInactiveProduct'),
        migrations.DeleteModel(name='OriginalPackaging'),
        migrations.DeleteModel(name='OriginalPharmaceuticalStandard'),
        migrations.DeleteModel(name='OriginalRoute'),
        migrations.DeleteModel(name='OriginalSchedule'),
        migrations.DeleteModel(name='OriginalStatus'),
        migrations.DeleteModel(name='OriginalTherapeuticClass'),
        migrations.DeleteModel(name='OriginalVeterinarySpecies'),

    ]
