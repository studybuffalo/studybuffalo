# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveIngredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_ingredient_code', models.CharField(blank=True, max_length=5, null=True)),
                ('ingredient', models.CharField(blank=True, max_length=240, null=True)),
                ('ingredient_supplied_ind', models.CharField(blank=True, max_length=1, null=True)),
                ('strength', models.CharField(blank=True, max_length=20, null=True)),
                ('strength_unit', models.CharField(blank=True, max_length=40, null=True)),
                ('strength_type', models.CharField(blank=True, max_length=40, null=True)),
                ('dosage_value', models.CharField(blank=True, max_length=20, null=True)),
                ('base', models.BooleanField()),
                ('dosage_unit', models.CharField(blank=True, max_length=40, null=True)),
                ('notes', models.CharField(blank=True, max_length=2000, null=True)),
                ('ingredient_f', models.CharField(blank=True, max_length=260, null=True)),
                ('strength_unit_f', models.CharField(blank=True, max_length=80, null=True)),
                ('strength_type_f', models.CharField(blank=True, max_length=80, null=True)),
                ('dosage_unit_f', models.CharField(blank=True, max_length=80, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mfr_code', models.CharField(blank=True, max_length=5, null=True)),
                ('company_code', models.PositiveIntegerField(blank=True, null=True)),
                ('company_name', models.CharField(blank=True, max_length=90, null=True)),
                ('company_type', models.CharField(blank=True, max_length=40, null=True)),
                ('address_mailing_flag', models.BooleanField()),
                ('address_billing_flag', models.BooleanField()),
                ('address_notification_flag', models.BooleanField()),
                ('address_other', models.BooleanField()),
                ('suite_number', models.CharField(blank=True, max_length=20, null=True)),
                ('street_name', models.CharField(blank=True, max_length=80, null=True)),
                ('city_name', models.CharField(blank=True, max_length=60, null=True)),
                ('province', models.CharField(blank=True, max_length=40, null=True)),
                ('country', models.CharField(blank=True, max_length=40, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True)),
                ('post_office_box', models.CharField(blank=True, max_length=15, null=True)),
                ('province_f', models.CharField(blank=True, max_length=40, null=True)),
                ('country_f', models.CharField(blank=True, max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DPD',
            fields=[
                (
                    'drug_code',
                    models.PositiveIntegerField(primary_key=True, serialize=False),
                ),
                (
                    'origin_file',
                    models.CharField(
                        choices=[('a', 'approved'), ('c', 'cancelled'), ('d', 'dormant'), ('m', 'marketed')],
                        max_length=1,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='DrugProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_categorization', models.CharField(blank=True, max_length=80, null=True)),
                ('class_e', models.CharField(blank=True, max_length=40, null=True)),
                ('drug_identification_number', models.CharField(blank=True, max_length=8, null=True)),
                ('brand_name', models.CharField(blank=True, max_length=200, null=True)),
                ('descriptor', models.CharField(blank=True, max_length=210, null=True)),
                ('pediatric_flag', models.BooleanField()),
                ('accession_number', models.CharField(blank=True, max_length=5, null=True)),
                ('number_of_ais', models.CharField(blank=True, max_length=10, null=True)),
                ('last_update_date', models.DateField(blank=True, null=True)),
                ('ai_group_no', models.CharField(blank=True, max_length=10, null=True)),
                ('class_f', models.CharField(blank=True, max_length=40, null=True)),
                ('brand_name_f', models.CharField(blank=True, max_length=200, null=True)),
                ('descriptor_f', models.CharField(blank=True, max_length=150, null=True)),
                ('drug_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.DPD')),
            ],
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pharm_form_code', models.PositiveIntegerField(blank=True, null=True)),
                ('pharmaceutical_form', models.CharField(blank=True, max_length=40, null=True)),
                ('pharmaceutical_form_f', models.CharField(blank=True, max_length=60, null=True)),
                ('drug_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.DPD')),
            ],
        ),
        migrations.CreateModel(
            name='InactiveProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_identification_number', models.CharField(blank=True, max_length=8, null=True)),
                ('brand_name', models.CharField(blank=True, max_length=200, null=True)),
                ('history_date', models.DateField(blank=True, null=True)),
                ('drug_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.DPD')),
            ],
        ),
        migrations.CreateModel(
            name='Packaging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upc', models.CharField(blank=True, max_length=12, null=True)),
                ('package_size_unit', models.CharField(blank=True, max_length=40, null=True)),
                ('package_type', models.CharField(blank=True, max_length=40, null=True)),
                ('package_size', models.CharField(blank=True, max_length=10, null=True)),
                ('product_information', models.CharField(blank=True, max_length=90, null=True)),
                ('package_size_unit_f', models.CharField(blank=True, max_length=80, null=True)),
                ('package_type_f', models.CharField(blank=True, max_length=80, null=True)),
                ('drug_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.DPD')),
            ],
        ),
        migrations.CreateModel(
            name='PharmaceuticalStandard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pharmaceutical_std', models.CharField(blank=True, max_length=40, null=True)),
                ('drug_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.DPD')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_of_administration_code', models.PositiveIntegerField(blank=True, null=True)),
                ('route_of_administration', models.CharField(blank=True, max_length=40, null=True)),
                ('route_of_administration_f', models.CharField(blank=True, max_length=60, null=True)),
                ('drug_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.DPD')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule', models.CharField(blank=True, max_length=40, null=True)),
                ('schedule_f', models.CharField(blank=True, max_length=40, null=True)),
                ('drug_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.DPD')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_status_flag', models.BooleanField()),
                ('status', models.CharField(blank=True, max_length=40, null=True)),
                ('history_date', models.DateField(blank=True, null=True)),
                ('status_f', models.CharField(blank=True, max_length=80, null=True)),
                ('lot_number', models.CharField(blank=True, max_length=80, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('drug_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.DPD')),
            ],
        ),
        migrations.CreateModel(
            name='SubAHFS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=80, unique=True)),
                ('substitution', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='SubAHFSPend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=80, unique=True)),
                ('substitution', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='TherapeuticClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tc_atc_number', models.CharField(blank=True, max_length=8, null=True)),
                ('tc_atc', models.CharField(blank=True, max_length=120, null=True)),
                ('tc_ahfs_number', models.CharField(blank=True, max_length=20, null=True)),
                ('tc_ahfs', models.CharField(blank=True, max_length=80, null=True)),
                ('tc_atc_f', models.CharField(blank=True, max_length=120, null=True)),
                ('tc_ahfs_f', models.CharField(blank=True, max_length=80, null=True)),
                ('drug_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.DPD')),
            ],
        ),
        migrations.CreateModel(
            name='VeterinarySpecies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vet_species', models.CharField(blank=True, max_length=80, null=True)),
                ('vet_sub_species', models.CharField(blank=True, max_length=80, null=True)),
                ('vet_species_f', models.CharField(blank=True, max_length=80, null=True)),
                ('drug_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.DPD')),
            ],
        ),
        migrations.AddField(
            model_name='companies',
            name='drug_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.DPD'),
        ),
        migrations.AddField(
            model_name='activeingredients',
            name='drug_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hc_dpd.DPD'),
        ),
    ]
