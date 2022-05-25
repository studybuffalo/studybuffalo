# pylint: disable=missing-module-docstring, missing-class-docstring, line-too-long
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('hc_dpd', '0015_additional_model_updates_for_api'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SubAHFS',
        ),
        migrations.DeleteModel(
            name='SubAHFSPend',
        ),
        migrations.AlterModelOptions(
            name='dpd',
            options={'permissions': (('api_view', 'Can view DPD data via the API'), ('api_edit', 'Can edit DPD data via the API'), ('web_view', 'Can view DPD data via the web views')), 'verbose_name': 'DPD code', 'verbose_name_plural': 'DPD codes'},
        ),
        migrations.AlterModelOptions(
            name='dpdchecksum',
            options={'verbose_name': 'DPD checksum', 'verbose_name_plural': 'DPD checksums'},
        ),
        migrations.AlterModelOptions(
            name='formattedactiveingredient',
            options={'verbose_name': 'formatted active ingredient', 'verbose_name_plural': 'formatted active ingredients'},
        ),
        migrations.AlterModelOptions(
            name='formattedbiosimilar',
            options={'verbose_name': 'formatted biosimilar', 'verbose_name_plural': 'formatted biosimilars'},
        ),
        migrations.AlterModelOptions(
            name='formattedcompany',
            options={'verbose_name': 'formatted company', 'verbose_name_plural': 'formatted companies'},
        ),
        migrations.AlterModelOptions(
            name='formatteddrugproduct',
            options={'verbose_name': 'formatted drug product', 'verbose_name_plural': 'formatted drug products'},
        ),
        migrations.AlterModelOptions(
            name='formattedform',
            options={'verbose_name': 'formatted form', 'verbose_name_plural': 'formatted forms'},
        ),
        migrations.AlterModelOptions(
            name='formattedinactiveproduct',
            options={'verbose_name': 'formatted inactive product', 'verbose_name_plural': 'formatted inactive products'},
        ),
        migrations.AlterModelOptions(
            name='formattedpackaging',
            options={'verbose_name': 'formatted packaging', 'verbose_name_plural': 'formatted packaging'},
        ),
        migrations.AlterModelOptions(
            name='formattedpharmaceuticalstandard',
            options={'verbose_name': 'formatted pharmaceutical standard', 'verbose_name_plural': 'formatted pharmaceutical standards'},
        ),
        migrations.AlterModelOptions(
            name='formattedroute',
            options={'verbose_name': 'formatted route', 'verbose_name_plural': 'formatted routes'},
        ),
        migrations.AlterModelOptions(
            name='formattedschedule',
            options={'verbose_name': 'formatted schedule', 'verbose_name_plural': 'formatted schedules'},
        ),
        migrations.AlterModelOptions(
            name='formattedstatus',
            options={'verbose_name': 'formatted status', 'verbose_name_plural': 'formatted statuses'},
        ),
        migrations.AlterModelOptions(
            name='formattedtherapeuticclass',
            options={'verbose_name': 'formatted therapeutic class', 'verbose_name_plural': 'formatted therapeutic classes'},
        ),
        migrations.AlterModelOptions(
            name='formattedveterinaryspecies',
            options={'verbose_name': 'formatted veterinary species', 'verbose_name_plural': 'formatted veterinary species'},
        ),
        migrations.AlterModelOptions(
            name='originalactiveingredient',
            options={'verbose_name': 'original active ingredient', 'verbose_name_plural': 'original active ingredients'},
        ),
        migrations.AlterModelOptions(
            name='originalbiosimilar',
            options={'verbose_name': 'original biosimilar', 'verbose_name_plural': 'original biosimilars'},
        ),
        migrations.AlterModelOptions(
            name='originalcompany',
            options={'verbose_name': 'original company', 'verbose_name_plural': 'original companies'},
        ),
        migrations.AlterModelOptions(
            name='originaldrugproduct',
            options={'verbose_name': 'original drug product', 'verbose_name_plural': 'original drug products'},
        ),
        migrations.AlterModelOptions(
            name='originalform',
            options={'verbose_name': 'original form', 'verbose_name_plural': 'original forms'},
        ),
        migrations.AlterModelOptions(
            name='originalinactiveproduct',
            options={'verbose_name': 'original inactive product', 'verbose_name_plural': 'original inactive products'},
        ),
        migrations.AlterModelOptions(
            name='originalpackaging',
            options={'verbose_name': 'original packaging', 'verbose_name_plural': 'original packaging'},
        ),
        migrations.AlterModelOptions(
            name='originalpharmaceuticalstandard',
            options={'verbose_name': 'original pharmaceutical standard', 'verbose_name_plural': 'original pharmaceutical standards'},
        ),
        migrations.AlterModelOptions(
            name='originalroute',
            options={'verbose_name': 'original route', 'verbose_name_plural': 'original routes'},
        ),
        migrations.AlterModelOptions(
            name='originalschedule',
            options={'verbose_name': 'original schedule', 'verbose_name_plural': 'original schedules'},
        ),
        migrations.AlterModelOptions(
            name='originalstatus',
            options={'verbose_name': 'original status', 'verbose_name_plural': 'original statuses'},
        ),
        migrations.AlterModelOptions(
            name='originaltherapeuticclass',
            options={'verbose_name': 'original therapeutic class', 'verbose_name_plural': 'original therapeutic classes'},
        ),
        migrations.AlterModelOptions(
            name='originalveterinaryspecies',
            options={'verbose_name': 'original veterinary species', 'verbose_name_plural': 'original veterinary species'},
        ),
    ]
