# pylint: disable=missing-module-docstring, missing-class-docstring, line-too-long
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0013_rename_models_as_original'),
    ]

    operations = [
        migrations.CreateModel(
            name='DPDChecksum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_code_start', models.PositiveIntegerField(help_text='The starting Health Canada Drug code for this checksum.')),
                ('drug_code_step', models.PositiveIntegerField(choices=[(1, 1), (10, 10), (100, 100), (1000, 1000), (10000, 10000), (100000, 100000)], help_text='The interval of drug codes for this checksum.')),
                ('extract_source', models.CharField(choices=[('active_ingredient', 'QRYM_ACTIVE_INGREDIENTS'), ('biosimilar', 'QRYM_BIOSIMILARS'), ('company', 'QRYM_COMPANIES'), ('drug_product', 'QRYM_DRUG_PRODUCT'), ('form', 'QRYM_FORM'), ('inactive_product', 'QRYM_INACTIVE_PRODUCTS'), ('packaging', 'QRYM_PACKAGING'), ('pharmaceutical_standard', 'QRYM_PHARMACEUTICAL_STD'), ('route', 'QRYM_ROUTE'), ('schedule', 'QRYM_SCHEDULE'), ('status', 'QRYM_STATUS'), ('therapeutic_class', 'QRYM_THERAPEUTIC_CLASS'), ('veterinary_species', 'QRYM_VETERINARY_SPECIES')], help_text='The extract source data for this checksum', max_length=32)),
                ('checksum', models.CharField(help_text='The checksum value for the specified items.', max_length=10)),
                ('checksum_date', models.DateField(auto_now=True, help_text='The date this checksum was created or updated.')),
            ],
        ),
        migrations.AlterModelOptions(
            name='dpd',
            options={'permissions': (('api_view', 'Can view DPD data via the API'), ('api_edit', 'Can edit DPD data via the API'))},
        ),
        migrations.AddField(
            model_name='dpd',
            name='original_active_ingredient_modified',
            field=models.DateTimeField(blank=True, help_text='When the original active ingredient instances were last modified.', null=True),
        ),
        migrations.AddField(
            model_name='dpd',
            name='original_biosimilars_modified',
            field=models.DateTimeField(blank=True, help_text='When the original biosimilar instances were last modified.', null=True),
        ),
        migrations.AddField(
            model_name='dpd',
            name='original_company_modified',
            field=models.DateTimeField(blank=True, help_text='When the original company instances were last modified.', null=True),
        ),
        migrations.AddField(
            model_name='dpd',
            name='original_drug_product_modified',
            field=models.DateTimeField(blank=True, help_text='When the original drug product instances were last modified.', null=True),
        ),
        migrations.AddField(
            model_name='dpd',
            name='original_form_modified',
            field=models.DateTimeField(blank=True, help_text='When the original form instances were last modified.', null=True),
        ),
        migrations.AddField(
            model_name='dpd',
            name='original_inactive_product_modified',
            field=models.DateTimeField(blank=True, help_text='When the original inactive product instances were last modified.', null=True),
        ),
        migrations.AddField(
            model_name='dpd',
            name='original_packaging_modified',
            field=models.DateTimeField(blank=True, help_text='When the original packaging instances were last modified.', null=True),
        ),
        migrations.AddField(
            model_name='dpd',
            name='original_pharmaceutical_standard_modified',
            field=models.DateTimeField(blank=True, help_text='When the original pharmaceutical standard instances were last modified.', null=True),
        ),
        migrations.AddField(
            model_name='dpd',
            name='original_route_modified',
            field=models.DateTimeField(blank=True, help_text='When the original route instances were last modified.', null=True),
        ),
        migrations.AddField(
            model_name='dpd',
            name='original_schedule_modified',
            field=models.DateTimeField(blank=True, help_text='When the original schedule instances were last modified.', null=True),
        ),
        migrations.AddField(
            model_name='dpd',
            name='original_status_modified',
            field=models.DateTimeField(blank=True, help_text='When the original status instances were last modified.', null=True),
        ),
        migrations.AddField(
            model_name='dpd',
            name='original_therapeutic_class_modified',
            field=models.DateTimeField(blank=True, help_text='When the original therapeutic_class instances were last modified.', null=True),
        ),
        migrations.AddField(
            model_name='dpd',
            name='original_veterinary_species_modified',
            field=models.DateTimeField(blank=True, help_text='When the original veterinary species instances were last modified.', null=True),
        ),
        migrations.AlterField(
            model_name='dpd',
            name='drug_code',
            field=models.PositiveIntegerField(help_text='The Health Canada Drug Code.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='active_ingredient_code',
            field=models.CharField(blank=True, help_text='The ACTIVE_INGREDIENT_CODE entry for this item.', max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='base',
            field=models.CharField(blank=True, help_text='The BASE entry for this item.', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='dosage_unit',
            field=models.CharField(blank=True, help_text='The DOSAGE_UNIT entry for this item.', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='dosage_unit_f',
            field=models.CharField(blank=True, help_text='The DOSAGE_UNIT_F entry for this item.', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='dosage_value',
            field=models.CharField(blank=True, help_text='The DOSAGE_VALUE entry for this item.', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='active_ingredients', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='ingredient',
            field=models.CharField(blank=True, help_text='The INGREDIENT entry for this item.', max_length=240, null=True),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='ingredient_f',
            field=models.CharField(blank=True, help_text='The INGREDIENT_F entry for this item.', max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='ingredient_supplied_ind',
            field=models.CharField(blank=True, help_text='The INGREDIENT_SUPPLIED_IND entry for this item.', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='notes',
            field=models.CharField(blank=True, help_text='The NOTES entry for this item.', max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='strength',
            field=models.CharField(blank=True, help_text='The STRENGTH entry for this item.', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='strength_type',
            field=models.CharField(blank=True, help_text='The STRENGTH_TYPE entry for this item.', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='strength_type_f',
            field=models.CharField(blank=True, help_text='The STRENGTH_TYPE_F entry for this item.', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='strength_unit',
            field=models.CharField(blank=True, help_text='The STRENGTH_UNIT entry for this item.', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='strength_unit_f',
            field=models.CharField(blank=True, help_text='The STRENGTH_UNIT_F entry for this item.', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='address_billing_flag',
            field=models.CharField(blank=True, help_text='The ADDRESS_BILLING_FLAG entry for this item.', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='address_mailing_flag',
            field=models.CharField(blank=True, help_text='The ADDRESS_MAILING_FLAG entry for this item.', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='address_notification_flag',
            field=models.CharField(blank=True, help_text='The ADDRESS_NOTIFICATION_FLAG entry for this item.', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='address_other',
            field=models.CharField(blank=True, help_text='The ADDRESS_OTHER entry for this item.', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='city_name',
            field=models.CharField(blank=True, help_text='The CITY_NAME entry for this item.', max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='company_code',
            field=models.PositiveIntegerField(blank=True, help_text='The COMPANY_CODE entry for this item.', null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='company_name',
            field=models.CharField(blank=True, help_text='The COMPANY_NAME entry for this item.', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='company_type',
            field=models.CharField(blank=True, help_text='The COMPANY_TYPE entry for this item.', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='country',
            field=models.CharField(blank=True, help_text='The COUNTRY entry for this item.', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='country_f',
            field=models.CharField(blank=True, help_text='The COUNTRY_F entry for this item.', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='mfr_code',
            field=models.CharField(blank=True, help_text='The MFR_CODE entry for this item.', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='post_office_box',
            field=models.CharField(blank=True, help_text='The POST_OFFICE_BOX entry for this item.', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='postal_code',
            field=models.CharField(blank=True, help_text='The POSTAL_CODE entry for this item.', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='province',
            field=models.CharField(blank=True, help_text='The PROVINCE entry for this item.', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='province_f',
            field=models.CharField(blank=True, help_text='The PROVINCE_F entry for this item.', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='street_name',
            field=models.CharField(blank=True, help_text='The STREET_NAME entry for this item.', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='suite_number',
            field=models.CharField(blank=True, help_text='The SUITE_NUMBER entry for this item.', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='originaldrugproduct',
            name='accession_number',
            field=models.CharField(blank=True, help_text='The ACCESSION_NUMBER entry for this item.', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='originaldrugproduct',
            name='ai_group_no',
            field=models.CharField(blank=True, help_text='The AI_GROUP_NO entry for this item.', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='originaldrugproduct',
            name='brand_name',
            field=models.CharField(blank=True, help_text='The BRAND_NAME entry for this item.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='originaldrugproduct',
            name='brand_name_f',
            field=models.CharField(blank=True, help_text='The BRAND_NAME_F entry for this item.', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='originaldrugproduct',
            name='class_e',
            field=models.CharField(blank=True, help_text='The CLASS entry for this item.', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='originaldrugproduct',
            name='class_f',
            field=models.CharField(blank=True, help_text='The CLASS_F entry for this item.', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='originaldrugproduct',
            name='descriptor',
            field=models.CharField(blank=True, help_text='The DESCRIPTOR entry for this item.', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='originaldrugproduct',
            name='descriptor_f',
            field=models.CharField(blank=True, help_text='The DESCRIPTOR_F entry for this item.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='originaldrugproduct',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originaldrugproduct',
            name='drug_identification_number',
            field=models.CharField(blank=True, help_text='The DRUG_IDENTIFICATION_NUMBER entry for this item.', max_length=29, null=True),
        ),
        migrations.AlterField(
            model_name='originaldrugproduct',
            name='last_update_date',
            field=models.DateField(blank=True, help_text='The LAST_UPDATE_DATE entry for this item.', null=True),
        ),
        migrations.AlterField(
            model_name='originaldrugproduct',
            name='number_of_ais',
            field=models.CharField(blank=True, help_text='The NUMBER_OF_AIS entry for this item.', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='originaldrugproduct',
            name='pediatric_flag',
            field=models.CharField(blank=True, help_text='The PEDIATRIC_FLAG entry for this item.', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='originaldrugproduct',
            name='product_categorization',
            field=models.CharField(blank=True, help_text='The PRODUCT_CATEGORIZATION entry for this item.', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='originalform',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalform',
            name='pharm_form_code',
            field=models.PositiveIntegerField(blank=True, help_text='The PHARM_FORM_CODE entry for this item.', null=True),
        ),
        migrations.AlterField(
            model_name='originalform',
            name='pharmaceutical_form',
            field=models.CharField(blank=True, help_text='The PHARMACEUTICAL_FORM entry for this item.', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='originalform',
            name='pharmaceutical_form_f',
            field=models.CharField(blank=True, help_text='The PHARMACEUTICAL_FORM_F entry for this item.', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='originalinactiveproduct',
            name='brand_name',
            field=models.CharField(blank=True, help_text='The BRAND_NAME entry for this item.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='originalinactiveproduct',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalinactiveproduct',
            name='drug_identification_number',
            field=models.CharField(blank=True, help_text='The DRUG_IDENTIFICATION_NUMBER entry for this item.', max_length=29, null=True),
        ),
        migrations.AlterField(
            model_name='originalinactiveproduct',
            name='history_date',
            field=models.DateField(blank=True, help_text='The HISTORY_DATE entry for this item.', null=True),
        ),
        migrations.AlterField(
            model_name='originalpackaging',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalpackaging',
            name='package_size',
            field=models.CharField(blank=True, help_text='The PACKAGE_SIZE entry for this item.', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='originalpackaging',
            name='package_size_unit',
            field=models.CharField(blank=True, help_text='The PACKAGE_SIZE_UNIT entry for this item.', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='originalpackaging',
            name='package_size_unit_f',
            field=models.CharField(blank=True, help_text='The PACKAGE_SIZE_UNIT_F entry for this item.', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='originalpackaging',
            name='package_type',
            field=models.CharField(blank=True, help_text='The PACKAGE_TYPE entry for this item.', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='originalpackaging',
            name='package_type_f',
            field=models.CharField(blank=True, help_text='The PACKAGE_TYPE_F entry for this item.', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='originalpackaging',
            name='product_information',
            field=models.CharField(blank=True, help_text='The PRODUCT_INFORMATION entry for this item.', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='originalpackaging',
            name='upc',
            field=models.CharField(blank=True, help_text='The UPC entry for this item.', max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='originalpharmaceuticalstandard',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalpharmaceuticalstandard',
            name='pharmaceutical_std',
            field=models.CharField(blank=True, help_text='The PHARMACEUTICAL_STD entry for this item.', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='originalroute',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalroute',
            name='route_of_administration',
            field=models.CharField(blank=True, help_text='The ROUTE_OF_ADMINISTRATION entry for this item.', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='originalroute',
            name='route_of_administration_code',
            field=models.PositiveIntegerField(blank=True, help_text='The ROUTE_OF_ADMINISTRATION_CODE entry for this item.', null=True),
        ),
        migrations.AlterField(
            model_name='originalroute',
            name='route_of_administration_f',
            field=models.CharField(blank=True, help_text='The ROUTE_OF_ADMINISTRATION_FFootnote entry for this item.', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='originalschedule',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalschedule',
            name='schedule',
            field=models.CharField(blank=True, help_text='The SCHEDULE entry for this item.', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='originalschedule',
            name='schedule_f',
            field=models.CharField(blank=True, help_text='The SCHEDULE_F entry for this item.', max_length=160, null=True),
        ),
        migrations.AlterField(
            model_name='originalstatus',
            name='current_status_flag',
            field=models.CharField(blank=True, help_text='The CURRENT_STATUS_FLAG entry for this item.', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='originalstatus',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalstatus',
            name='expiration_date',
            field=models.DateField(blank=True, help_text='The EXPIRATION_DATEFootnote entry for this item.', null=True),
        ),
        migrations.AlterField(
            model_name='originalstatus',
            name='history_date',
            field=models.DateField(blank=True, help_text='The HISTORY_DATE entry for this item.', null=True),
        ),
        migrations.AlterField(
            model_name='originalstatus',
            name='lot_number',
            field=models.CharField(blank=True, help_text='The LOT_NUMBER entry for this item.', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='originalstatus',
            name='status',
            field=models.CharField(blank=True, help_text='The STATUS entry for this item.', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='originalstatus',
            name='status_f',
            field=models.CharField(blank=True, help_text='The STATUS_F entry for this item.', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='originaltherapeuticclass',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originaltherapeuticclass',
            name='tc_atc',
            field=models.CharField(blank=True, help_text='The TC_ATC entry for this item.', max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='originaltherapeuticclass',
            name='tc_atc_f',
            field=models.CharField(blank=True, help_text='The TC_ATC_F entry for this item.', max_length=240, null=True),
        ),
        migrations.AlterField(
            model_name='originaltherapeuticclass',
            name='tc_atc_number',
            field=models.CharField(blank=True, help_text='The TC_ATC_NUMBER entry for this item.', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='originalveterinaryspecies',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalveterinaryspecies',
            name='vet_species',
            field=models.CharField(blank=True, help_text='The VET_SPECIES entry for this item.', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='originalveterinaryspecies',
            name='vet_species_f',
            field=models.CharField(blank=True, help_text='The VET_SPECIES_F entry for this item.', max_length=160, null=True),
        ),
        migrations.AlterField(
            model_name='originalveterinaryspecies',
            name='vet_sub_species',
            field=models.CharField(blank=True, help_text='The VET_SUB_SPECIES entry for this item.', max_length=80, null=True),
        ),
        migrations.CreateModel(
            name='OriginalBiosimilar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biosimilar_code', models.PositiveIntegerField(blank=True, help_text='The BIOSIMILAR_CODE entry for this item.', null=True)),
                ('biosimilar_type', models.CharField(blank=True, help_text='The BIOSIMILAR_TYPE entry for this item.', max_length=20, null=True)),
                ('biosimilar_type_F', models.CharField(blank=True, help_text='The BIOSIMILAR_TYPE_F entry for this item.', max_length=20, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd')),
            ],
        ),
        migrations.CreateModel(
            name='FormattedVeterinarySpecies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vet_species', models.CharField(blank=True, help_text='The formatted version of VET_SPECIES.', max_length=80, null=True)),
                ('vet_sub_species', models.CharField(blank=True, help_text='The formatted version of VET_SUB_SPECIES.', max_length=80, null=True)),
                ('vet_species_f', models.CharField(blank=True, help_text='The formatted version of VET_SPECIES_F.', max_length=160, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd')),
            ],
        ),
        migrations.CreateModel(
            name='FormattedTherapeuticClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tc_atc_number', models.CharField(blank=True, help_text='The formatted version of TC_ATC_NUMBER.', max_length=8, null=True)),
                ('tc_atc', models.CharField(blank=True, help_text='The formatted version of TC_ATC.', max_length=120, null=True)),
                ('tc_atc_f', models.CharField(blank=True, help_text='The formatted version of TC_ATC_F.', max_length=240, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd')),
            ],
        ),
        migrations.CreateModel(
            name='FormattedStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_status_flag', models.CharField(blank=True, help_text='The formatted version of CURRENT_STATUS_FLAG.', max_length=1, null=True)),
                ('status', models.CharField(blank=True, help_text='The formatted version of STATUS.', max_length=40, null=True)),
                ('history_date', models.DateField(blank=True, help_text='The formatted version of HISTORY_DATE.', null=True)),
                ('status_f', models.CharField(blank=True, help_text='The formatted version of STATUS_F.', max_length=80, null=True)),
                ('lot_number', models.CharField(blank=True, help_text='The formatted version of LOT_NUMBER.', max_length=50, null=True)),
                ('expiration_date', models.DateField(blank=True, help_text='The formatted version of EXPIRATION_DATE.', null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd')),
            ],
        ),
        migrations.CreateModel(
            name='FormattedSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule', models.CharField(blank=True, help_text='The formatted version of SCHEDULE.', max_length=40, null=True)),
                ('schedule_f', models.CharField(blank=True, help_text='The formatted version of SCHEDULE_F.', max_length=160, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd')),
            ],
        ),
        migrations.CreateModel(
            name='FormattedRoute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_of_administration_code', models.PositiveIntegerField(blank=True, help_text='The formatted version of ROUTE_OF_ADMINISTRATION_CODE.', null=True)),
                ('route_of_administration', models.CharField(blank=True, help_text='The formatted version of ROUTE_OF_ADMINISTRATION.', max_length=40, null=True)),
                ('route_of_administration_f', models.CharField(blank=True, help_text='The formatted version of ROUTE_OF_ADMINISTRATION_F.', max_length=80, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd')),
            ],
        ),
        migrations.CreateModel(
            name='FormattedPharmaceuticalStandard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pharmaceutical_std', models.CharField(blank=True, help_text='The formatted version of PHARMACEUTICAL_STD.', max_length=40, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd')),
            ],
        ),
        migrations.CreateModel(
            name='FormattedPackaging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upc', models.CharField(blank=True, help_text='The formatted version of UPC.', max_length=12, null=True)),
                ('package_size_unit', models.CharField(blank=True, help_text='The formatted version of PACKAGE_SIZE_UNIT.', max_length=40, null=True)),
                ('package_type', models.CharField(blank=True, help_text='The formatted version of PACKAGE_TYPE.', max_length=40, null=True)),
                ('package_size', models.CharField(blank=True, help_text='The formatted version of PACKAGE_SIZE.', max_length=5, null=True)),
                ('product_information', models.CharField(blank=True, help_text='The formatted version of PRODUCT_INFORMATION.', max_length=80, null=True)),
                ('package_size_unit_f', models.CharField(blank=True, help_text='The formatted version of PACKAGE_SIZE_UNIT_F.', max_length=80, null=True)),
                ('package_type_f', models.CharField(blank=True, help_text='The formatted version of PACKAGE_TYPE_F.', max_length=80, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd')),
            ],
        ),
        migrations.CreateModel(
            name='FormattedInactiveProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_identification_number', models.CharField(blank=True, help_text='The formatted version of DRUG_IDENTIFICATION_NUMBER.', max_length=29, null=True)),
                ('brand_name', models.CharField(blank=True, help_text='The formatted version of BRAND_NAME.', max_length=200, null=True)),
                ('history_date', models.DateField(blank=True, help_text='The formatted version of HISTORY_DATE.', null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd')),
            ],
        ),
        migrations.CreateModel(
            name='FormattedForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pharm_form_code', models.PositiveIntegerField(blank=True, help_text='The formatted version of PHARM_FORM_CODE.', null=True)),
                ('pharmaceutical_form', models.CharField(blank=True, help_text='The formatted version of PHARMACEUTICAL_FORM.', max_length=40, null=True)),
                ('pharmaceutical_form_f', models.CharField(blank=True, help_text='The formatted version of PHARMACEUTICAL_FORM_F.', max_length=80, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd')),
            ],
        ),
        migrations.CreateModel(
            name='FormattedDrugProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_categorization', models.CharField(blank=True, help_text='The formatted version of PRODUCT_CATEGORIZATION.', max_length=80, null=True)),
                ('class_e', models.CharField(blank=True, help_text='The formatted version of CLASS.', max_length=40, null=True)),
                ('drug_identification_number', models.CharField(blank=True, help_text='The formatted version of DRUG_IDENTIFICATION_NUMBER.', max_length=29, null=True)),
                ('brand_name', models.CharField(blank=True, help_text='The formatted version of BRAND_NAME.', max_length=200, null=True)),
                ('descriptor', models.CharField(blank=True, help_text='The formatted version of DESCRIPTOR.', max_length=150, null=True)),
                ('pediatric_flag', models.CharField(blank=True, help_text='The formatted version of PEDIATRIC_FLAG.', max_length=1, null=True)),
                ('accession_number', models.CharField(blank=True, help_text='The formatted version of ACCESSION_NUMBER.', max_length=5, null=True)),
                ('number_of_ais', models.CharField(blank=True, help_text='The formatted version of NUMBER_OF_AIS.', max_length=10, null=True)),
                ('last_update_date', models.DateField(blank=True, help_text='The formatted version of LAST_UPDATE_DATE.', null=True)),
                ('ai_group_no', models.CharField(blank=True, help_text='The formatted version of AI_GROUP_NO.', max_length=10, null=True)),
                ('class_f', models.CharField(blank=True, help_text='The formatted version of CLASS_F.', max_length=80, null=True)),
                ('brand_name_f', models.CharField(blank=True, help_text='The formatted version of BRAND_NAME_F.', max_length=300, null=True)),
                ('descriptor_f', models.CharField(blank=True, help_text='The formatted version of DESCRIPTOR_F.', max_length=200, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd')),
            ],
        ),
        migrations.CreateModel(
            name='FormattedCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mfr_code', models.CharField(blank=True, help_text='The formatted version of MFR_CODE.', max_length=5, null=True)),
                ('company_code', models.PositiveIntegerField(blank=True, help_text='The formatted version of COMPANY_CODE.', null=True)),
                ('company_name', models.CharField(blank=True, help_text='The formatted version of COMPANY_NAME.', max_length=80, null=True)),
                ('company_type', models.CharField(blank=True, help_text='The formatted version of COMPANY_TYPE.', max_length=40, null=True)),
                ('address_mailing_flag', models.CharField(blank=True, help_text='The formatted version of ADDRESS_MAILING_FLAG.', max_length=1, null=True)),
                ('address_billing_flag', models.CharField(blank=True, help_text='The formatted version of ADDRESS_BILLING_FLAG.', max_length=1, null=True)),
                ('address_notification_flag', models.CharField(blank=True, help_text='The formatted version of ADDRESS_NOTIFICATION_FLAG.', max_length=1, null=True)),
                ('address_other', models.CharField(blank=True, help_text='The formatted version of ADDRESS_OTHER.', max_length=1, null=True)),
                ('suite_number', models.CharField(blank=True, help_text='The formatted version of SUITE_NUMBER.', max_length=20, null=True)),
                ('street_name', models.CharField(blank=True, help_text='The formatted version of STREET_NAME.', max_length=80, null=True)),
                ('city_name', models.CharField(blank=True, help_text='The formatted version of CITY_NAME.', max_length=60, null=True)),
                ('province', models.CharField(blank=True, help_text='The formatted version of PROVINCE.', max_length=40, null=True)),
                ('country', models.CharField(blank=True, help_text='The formatted version of COUNTRY.', max_length=40, null=True)),
                ('postal_code', models.CharField(blank=True, help_text='The formatted version of POSTAL_CODE.', max_length=20, null=True)),
                ('post_office_box', models.CharField(blank=True, help_text='The formatted version of POST_OFFICE_BOX.', max_length=15, null=True)),
                ('province_f', models.CharField(blank=True, help_text='The formatted version of PROVINCE_F.', max_length=100, null=True)),
                ('country_f', models.CharField(blank=True, help_text='The formatted version of COUNTRY_F.', max_length=100, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd')),
            ],
        ),
        migrations.CreateModel(
            name='FormattedBiosimilars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biosimilar_code', models.PositiveIntegerField(blank=True, help_text='The formatted version of BIOSIMILAR_CODE.', null=True)),
                ('biosimilar_type', models.CharField(blank=True, help_text='The formatted version of BIOSIMILAR_TYPE.', max_length=20, null=True)),
                ('biosimilar_type_F', models.CharField(blank=True, help_text='The formatted version of BIOSIMILAR_TYPE_F.', max_length=20, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd')),
            ],
        ),
        migrations.CreateModel(
            name='FormattedActiveIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_ingredient_code', models.CharField(blank=True, help_text='The formatted version of ACTIVE_INGREDIENT_CODE.', max_length=6, null=True)),
                ('ingredient', models.CharField(blank=True, help_text='The formatted version of INGREDIENT.', max_length=240, null=True)),
                ('ingredient_supplied_ind', models.CharField(blank=True, help_text='The formatted version of INGREDIENT_SUPPLIED_IND.', max_length=1, null=True)),
                ('strength', models.CharField(blank=True, help_text='The formatted version of STRENGTH.', max_length=20, null=True)),
                ('strength_unit', models.CharField(blank=True, help_text='The formatted version of STRENGTH_UNIT.', max_length=40, null=True)),
                ('strength_type', models.CharField(blank=True, help_text='The formatted version of STRENGTH_TYPE.', max_length=40, null=True)),
                ('dosage_value', models.CharField(blank=True, help_text='The formatted version of DOSAGE_VALUE.', max_length=20, null=True)),
                ('base', models.CharField(blank=True, help_text='The formatted version of BASE.', max_length=1, null=True)),
                ('dosage_unit', models.CharField(blank=True, help_text='The formatted version of DOSAGE_UNIT.', max_length=40, null=True)),
                ('notes', models.CharField(blank=True, help_text='The formatted version of NOTES.', max_length=2000, null=True)),
                ('ingredient_f', models.CharField(blank=True, help_text='The formatted version of INGREDIENT_F.', max_length=400, null=True)),
                ('strength_unit_f', models.CharField(blank=True, help_text='The formatted version of STRENGTH_UNIT_F.', max_length=80, null=True)),
                ('strength_type_f', models.CharField(blank=True, help_text='The formatted version of STRENGTH_TYPE_F.', max_length=80, null=True)),
                ('dosage_unit_f', models.CharField(blank=True, help_text='The formatted version of DOSAGE_UNIT_F.', max_length=80, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.dpd')),
            ],
        ),
    ]
