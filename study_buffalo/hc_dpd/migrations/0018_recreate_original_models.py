# pylint: disable=missing-module-docstring, missing-class-docstring, line-too-long
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0017_delete_original_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='OriginalVeterinarySpecies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vet_species', models.CharField(blank=True, help_text='The VET_SPECIES entry for this item.', max_length=80, null=True)),
                ('vet_sub_species', models.CharField(blank=True, help_text='The VET_SUB_SPECIES entry for this item.', max_length=80, null=True)),
                ('vet_species_f', models.CharField(blank=True, help_text='The VET_SPECIES_F entry for this item.', max_length=160, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_veterinary_species', to='hc_dpd.dpd')),
            ],
            options={
                'verbose_name': 'original veterinary species',
                'verbose_name_plural': 'original veterinary species',
            },
        ),
        migrations.CreateModel(
            name='OriginalTherapeuticClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tc_atc_number', models.CharField(blank=True, help_text='The TC_ATC_NUMBER entry for this item.', max_length=8, null=True)),
                ('tc_atc', models.CharField(blank=True, help_text='The TC_ATC entry for this item.', max_length=120, null=True)),
                ('tc_atc_f', models.CharField(blank=True, help_text='The TC_ATC_F entry for this item.', max_length=240, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_therapeutic_classes', to='hc_dpd.dpd')),
            ],
            options={
                'verbose_name': 'original therapeutic class',
                'verbose_name_plural': 'original therapeutic classes',
            },
        ),
        migrations.CreateModel(
            name='OriginalStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_status_flag', models.CharField(blank=True, help_text='The CURRENT_STATUS_FLAG entry for this item.', max_length=1, null=True)),
                ('status', models.CharField(blank=True, help_text='The STATUS entry for this item.', max_length=40, null=True)),
                ('history_date', models.CharField(blank=True, help_text='The HISTORY_DATE entry for this item.', max_length=11, null=True)),
                ('status_f', models.CharField(blank=True, help_text='The STATUS_F entry for this item.', max_length=80, null=True)),
                ('lot_number', models.CharField(blank=True, help_text='The LOT_NUMBER entry for this item.', max_length=50, null=True)),
                ('expiration_date', models.CharField(blank=True, help_text='The EXPIRATION_DATE entry for this item.', max_length=11, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_statuses', to='hc_dpd.dpd')),
            ],
            options={
                'verbose_name': 'original status',
                'verbose_name_plural': 'original statuses',
            },
        ),
        migrations.CreateModel(
            name='OriginalSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule', models.CharField(blank=True, help_text='The SCHEDULE entry for this item.', max_length=40, null=True)),
                ('schedule_f', models.CharField(blank=True, help_text='The SCHEDULE_F entry for this item.', max_length=160, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_schedules', to='hc_dpd.dpd')),
            ],
            options={
                'verbose_name': 'original schedule',
                'verbose_name_plural': 'original schedules',
            },
        ),
        migrations.CreateModel(
            name='OriginalRoute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_of_administration_code', models.CharField(blank=True, help_text='The ROUTE_OF_ADMINISTRATION_CODE entry for this item.', max_length=3, null=True)),
                ('route_of_administration', models.CharField(blank=True, help_text='The ROUTE_OF_ADMINISTRATION entry for this item.', max_length=40, null=True)),
                ('route_of_administration_f', models.CharField(blank=True, help_text='The ROUTE_OF_ADMINISTRATION_F entry for this item.', max_length=80, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_routes', to='hc_dpd.dpd')),
            ],
            options={
                'verbose_name': 'original route',
                'verbose_name_plural': 'original routes',
            },
        ),
        migrations.CreateModel(
            name='OriginalPharmaceuticalStandard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pharmaceutical_std', models.CharField(blank=True, help_text='The PHARMACEUTICAL_STD entry for this item.', max_length=40, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_pharmaceutical_standards', to='hc_dpd.dpd')),
            ],
            options={
                'verbose_name': 'original pharmaceutical standard',
                'verbose_name_plural': 'original pharmaceutical standards',
            },
        ),
        migrations.CreateModel(
            name='OriginalPackaging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upc', models.CharField(blank=True, help_text='The UPC entry for this item.', max_length=12, null=True)),
                ('package_size_unit', models.CharField(blank=True, help_text='The PACKAGE_SIZE_UNIT entry for this item.', max_length=40, null=True)),
                ('package_type', models.CharField(blank=True, help_text='The PACKAGE_TYPE entry for this item.', max_length=40, null=True)),
                ('package_size', models.CharField(blank=True, help_text='The PACKAGE_SIZE entry for this item.', max_length=5, null=True)),
                ('product_information', models.CharField(blank=True, help_text='The PRODUCT_INFORMATION entry for this item.', max_length=80, null=True)),
                ('package_size_unit_f', models.CharField(blank=True, help_text='The PACKAGE_SIZE_UNIT_F entry for this item.', max_length=80, null=True)),
                ('package_type_f', models.CharField(blank=True, help_text='The PACKAGE_TYPE_F entry for this item.', max_length=80, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_packaging', to='hc_dpd.dpd')),
            ],
            options={
                'verbose_name': 'original packaging',
                'verbose_name_plural': 'original packaging',
            },
        ),
        migrations.CreateModel(
            name='OriginalInactiveProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_identification_number', models.CharField(blank=True, help_text='The DRUG_IDENTIFICATION_NUMBER entry for this item.', max_length=29, null=True)),
                ('brand_name', models.CharField(blank=True, help_text='The BRAND_NAME entry for this item.', max_length=200, null=True)),
                ('history_date', models.CharField(blank=True, help_text='The HISTORY_DATE entry for this item.', max_length=11, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_inactive_products', to='hc_dpd.dpd')),
            ],
            options={
                'verbose_name': 'original inactive product',
                'verbose_name_plural': 'original inactive products',
            },
        ),
        migrations.CreateModel(
            name='OriginalForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pharm_form_code', models.CharField(blank=True, help_text='The PHARM_FORM_CODE entry for this item.', max_length=3, null=True)),
                ('pharmaceutical_form', models.CharField(blank=True, help_text='The PHARMACEUTICAL_FORM entry for this item.', max_length=40, null=True)),
                ('pharmaceutical_form_f', models.CharField(blank=True, help_text='The PHARMACEUTICAL_FORM_F entry for this item.', max_length=80, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_forms', to='hc_dpd.dpd')),
            ],
            options={
                'verbose_name': 'original form',
                'verbose_name_plural': 'original forms',
            },
        ),
        migrations.CreateModel(
            name='OriginalDrugProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_categorization', models.CharField(blank=True, help_text='The PRODUCT_CATEGORIZATION entry for this item.', max_length=80, null=True)),
                ('class_e', models.CharField(blank=True, help_text='The CLASS entry for this item.', max_length=40, null=True)),
                ('drug_identification_number', models.CharField(blank=True, help_text='The DRUG_IDENTIFICATION_NUMBER entry for this item.', max_length=29, null=True)),
                ('brand_name', models.CharField(blank=True, help_text='The BRAND_NAME entry for this item.', max_length=200, null=True)),
                ('descriptor', models.CharField(blank=True, help_text='The DESCRIPTOR entry for this item.', max_length=150, null=True)),
                ('pediatric_flag', models.CharField(blank=True, help_text='The PEDIATRIC_FLAG entry for this item.', max_length=1, null=True)),
                ('accession_number', models.CharField(blank=True, help_text='The ACCESSION_NUMBER entry for this item.', max_length=5, null=True)),
                ('number_of_ais', models.CharField(blank=True, help_text='The NUMBER_OF_AIS entry for this item.', max_length=10, null=True)),
                ('last_update_date', models.CharField(blank=True, help_text='The LAST_UPDATE_DATE entry for this item.', max_length=11, null=True)),
                ('ai_group_no', models.CharField(blank=True, help_text='The AI_GROUP_NO entry for this item.', max_length=10, null=True)),
                ('class_f', models.CharField(blank=True, help_text='The CLASS_F entry for this item.', max_length=80, null=True)),
                ('brand_name_f', models.CharField(blank=True, help_text='The BRAND_NAME_F entry for this item.', max_length=300, null=True)),
                ('descriptor_f', models.CharField(blank=True, help_text='The DESCRIPTOR_F entry for this item.', max_length=200, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_drug_products', to='hc_dpd.dpd')),
            ],
            options={
                'verbose_name': 'original drug product',
                'verbose_name_plural': 'original drug products',
            },
        ),
        migrations.CreateModel(
            name='OriginalCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mfr_code', models.CharField(blank=True, help_text='The MFR_CODE entry for this item.', max_length=5, null=True)),
                ('company_code', models.CharField(blank=True, help_text='The COMPANY_CODE entry for this item.', max_length=5, null=True)),
                ('company_name', models.CharField(blank=True, help_text='The COMPANY_NAME entry for this item.', max_length=80, null=True)),
                ('company_type', models.CharField(blank=True, help_text='The COMPANY_TYPE entry for this item.', max_length=40, null=True)),
                ('address_mailing_flag', models.CharField(blank=True, help_text='The ADDRESS_MAILING_FLAG entry for this item.', max_length=1, null=True)),
                ('address_billing_flag', models.CharField(blank=True, help_text='The ADDRESS_BILLING_FLAG entry for this item.', max_length=1, null=True)),
                ('address_notification_flag', models.CharField(blank=True, help_text='The ADDRESS_NOTIFICATION_FLAG entry for this item.', max_length=1, null=True)),
                ('address_other', models.CharField(blank=True, help_text='The ADDRESS_OTHER entry for this item.', max_length=1, null=True)),
                ('suite_number', models.CharField(blank=True, help_text='The SUITE_NUMBER entry for this item.', max_length=20, null=True)),
                ('street_name', models.CharField(blank=True, help_text='The STREET_NAME entry for this item.', max_length=80, null=True)),
                ('city_name', models.CharField(blank=True, help_text='The CITY_NAME entry for this item.', max_length=60, null=True)),
                ('province', models.CharField(blank=True, help_text='The PROVINCE entry for this item.', max_length=40, null=True)),
                ('country', models.CharField(blank=True, help_text='The COUNTRY entry for this item.', max_length=40, null=True)),
                ('postal_code', models.CharField(blank=True, help_text='The POSTAL_CODE entry for this item.', max_length=20, null=True)),
                ('post_office_box', models.CharField(blank=True, help_text='The POST_OFFICE_BOX entry for this item.', max_length=15, null=True)),
                ('province_f', models.CharField(blank=True, help_text='The PROVINCE_F entry for this item.', max_length=100, null=True)),
                ('country_f', models.CharField(blank=True, help_text='The COUNTRY_F entry for this item.', max_length=100, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_companies', to='hc_dpd.dpd')),
            ],
            options={
                'verbose_name': 'original company',
                'verbose_name_plural': 'original companies',
            },
        ),
        migrations.CreateModel(
            name='OriginalBiosimilar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biosimilar_code', models.CharField(blank=True, help_text='The BIOSIMILAR_CODE entry for this item.', max_length=3, null=True)),
                ('biosimilar_type', models.CharField(blank=True, help_text='The BIOSIMILAR_TYPE entry for this item.', max_length=20, null=True)),
                ('biosimilar_type_f', models.CharField(blank=True, help_text='The BIOSIMILAR_TYPE_F entry for this item.', max_length=20, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_biosimilars', to='hc_dpd.dpd')),
            ],
            options={
                'verbose_name': 'original biosimilar',
                'verbose_name_plural': 'original biosimilars',
            },
        ),
        migrations.CreateModel(
            name='OriginalActiveIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_ingredient_code', models.CharField(blank=True, help_text='The ACTIVE_INGREDIENT_CODE entry for this item.', max_length=6, null=True)),
                ('ingredient', models.CharField(blank=True, help_text='The INGREDIENT entry for this item.', max_length=240, null=True)),
                ('ingredient_supplied_ind', models.CharField(blank=True, help_text='The INGREDIENT_SUPPLIED_IND entry for this item.', max_length=1, null=True)),
                ('strength', models.CharField(blank=True, help_text='The STRENGTH entry for this item.', max_length=20, null=True)),
                ('strength_unit', models.CharField(blank=True, help_text='The STRENGTH_UNIT entry for this item.', max_length=40, null=True)),
                ('strength_type', models.CharField(blank=True, help_text='The STRENGTH_TYPE entry for this item.', max_length=40, null=True)),
                ('dosage_value', models.CharField(blank=True, help_text='The DOSAGE_VALUE entry for this item.', max_length=20, null=True)),
                ('base', models.CharField(blank=True, help_text='The BASE entry for this item.', max_length=1, null=True)),
                ('dosage_unit', models.CharField(blank=True, help_text='The DOSAGE_UNIT entry for this item.', max_length=40, null=True)),
                ('notes', models.CharField(blank=True, help_text='The NOTES entry for this item.', max_length=2000, null=True)),
                ('ingredient_f', models.CharField(blank=True, help_text='The INGREDIENT_F entry for this item.', max_length=400, null=True)),
                ('strength_unit_f', models.CharField(blank=True, help_text='The STRENGTH_UNIT_F entry for this item.', max_length=80, null=True)),
                ('strength_type_f', models.CharField(blank=True, help_text='The STRENGTH_TYPE_F entry for this item.', max_length=80, null=True)),
                ('dosage_unit_f', models.CharField(blank=True, help_text='The DOSAGE_UNIT_F entry for this item.', max_length=80, null=True)),
                ('drug_code', models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_active_ingredients', to='hc_dpd.dpd')),
            ],
            options={
                'verbose_name': 'original active ingredient',
                'verbose_name_plural': 'original active ingredients',
            },
        ),
    ]
