# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [
        ('drug_price_calculator', '0001_initial'),
        ('drug_price_calculator', '0002_subsbsrf_subsgeneric_subsmanufacturer_subsptc_subsunit'),
        ('drug_price_calculator', '0003_pendbsrf_pendgeneric_pendmanufacturer_pendptc'),
        ('drug_price_calculator', '0004_auto_20170916_0749'),
        ('drug_price_calculator', '0005_auto_20170919_2115'),
        ('drug_price_calculator', '0006_auto_20170920_1543'),
        ('drug_price_calculator', '0007_auto_20170920_1545'),
        ('drug_price_calculator', '0008_auto_20170920_1742'),
        ('drug_price_calculator', '0009_auto_20170920_2147'),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ATC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.PositiveIntegerField()),
                ('atc_1', models.CharField(max_length=7, null=True)),
                ('atc_1_text', models.CharField(max_length=200, null=True)),
                ('atc_2', models.CharField(max_length=7, null=True)),
                ('atc_2_text', models.CharField(max_length=200, null=True)),
                ('atc_3', models.CharField(max_length=7, null=True)),
                ('atc_3_text', models.CharField(max_length=200, null=True)),
                ('atc_4', models.CharField(max_length=7, null=True)),
                ('atc_4_text', models.CharField(max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Anatomical Therapeutic Category',
                'verbose_name_plural': 'Anatomical Therapeutic Categories',
            },
        ),
        migrations.CreateModel(
            name='ATCDescriptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5, unique=True)),
                ('description', models.CharField(max_length=80, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Coverage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.PositiveIntegerField()),
                ('coverage', models.CharField(max_length=50)),
                ('criteria', models.BooleanField()),
                ('criteria_sa', models.CharField(max_length=100, null=True)),
                ('criteria_p', models.CharField(max_length=70, null=True)),
                ('group_1', models.BooleanField(default=False)),
                ('group_66', models.BooleanField(default=False)),
                ('group_66a', models.BooleanField(default=False)),
                ('group_19823', models.BooleanField(default=False)),
                ('group_19823a', models.BooleanField(default=False)),
                ('group_19824', models.BooleanField(default=False)),
                ('group_20400', models.BooleanField(default=False)),
                ('group_20403', models.BooleanField(default=False)),
                ('group_20514', models.BooleanField(default=False)),
                ('group_22128', models.BooleanField(default=False)),
                ('group_23609', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExtraInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.PositiveIntegerField()),
                ('date_listed', models.DateField(null=True)),
                ('date_discontinued', models.DateField(null=True)),
                ('manufacturer', models.CharField(max_length=75)),
                ('schedule', models.CharField(max_length=10)),
                ('interchangeable', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.PositiveIntegerField()),
                ('din', models.PositiveIntegerField()),
                ('brand_name', models.CharField(max_length=70, null=True)),
                ('strength', models.CharField(max_length=200, null=True)),
                ('route', models.CharField(max_length=20, null=True)),
                ('dosage_form', models.CharField(max_length=35, null=True)),
                ('generic_name', models.CharField(max_length=450, null=True)),
                ('unit_price', models.DecimalField(decimal_places=4, max_digits=10, null=True)),
                ('lca', models.DecimalField(decimal_places=4, max_digits=10, null=True)),
                ('lca_text', models.CharField(max_length=150, null=True)),
                ('unit_issue', models.CharField(max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PTC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.PositiveIntegerField()),
                ('ptc_1', models.PositiveIntegerField(null=True)),
                ('ptc_1_text', models.CharField(max_length=75, null=True)),
                ('ptc_2', models.PositiveIntegerField(null=True)),
                ('ptc_2_text', models.CharField(max_length=75, null=True)),
                ('ptc_3', models.PositiveIntegerField(null=True)),
                ('ptc_3_text', models.CharField(max_length=75, null=True)),
                ('ptc_4', models.PositiveIntegerField(null=True)),
                ('ptc_4_text', models.CharField(max_length=75, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SpecialAuthorization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=200, null=True)),
                ('link', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubsBSRF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bsrf', models.CharField(max_length=250, unique=True)),
                ('brand_name', models.CharField(max_length=80)),
                ('strength', models.CharField(max_length=200, null=True)),
                ('route', models.CharField(max_length=20, null=True)),
                ('dosage_form', models.CharField(max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubsGeneric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=450, unique=True)),
                ('correction', models.CharField(max_length=450)),
            ],
        ),
        migrations.CreateModel(
            name='SubsManufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=120, unique=True)),
                ('correction', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='SubsPTC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=120, unique=True)),
                ('correction', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='SubsUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=120, unique=True)),
                ('correction', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='PendBSRF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=250, unique=True)),
                ('brand_name', models.CharField(max_length=80)),
                ('strength', models.CharField(max_length=200, null=True)),
                ('route', models.CharField(max_length=20, null=True)),
                ('dosage_form', models.CharField(max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PendGeneric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=450, unique=True)),
                ('correction', models.CharField(max_length=450)),
            ],
        ),
        migrations.CreateModel(
            name='PendManufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=150, unique=True)),
                ('correction', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='PendPTC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=150, unique=True)),
                ('correction', models.CharField(max_length=150)),
            ],
        ),
    ]
