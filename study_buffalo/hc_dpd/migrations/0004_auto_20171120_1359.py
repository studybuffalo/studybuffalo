# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0003_subahfs_subahfspend'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=200, unique=True)),
                ('substitution', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Substitution - Brand Name',
                'verbose_name_plural': 'Substitutions - Brand Name',
            },
        ),
        migrations.CreateModel(
            name='SubBrandPend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=200, unique=True)),
                ('substitution', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Substitution - Brand Name (Pending)',
                'verbose_name_plural': 'Substitutions - Brand Name (Pending)',
            },
        ),
        migrations.CreateModel(
            name='SubCompanyName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=90, unique=True)),
                ('substitution', models.CharField(max_length=90)),
            ],
            options={
                'verbose_name': 'Substitution - Company Name',
                'verbose_name_plural': 'Substitutions - Company Name',
            },
        ),
        migrations.CreateModel(
            name='SubCompanyNamePend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=90, unique=True)),
                ('substitution', models.CharField(max_length=90)),
            ],
            options={
                'verbose_name': 'Substitution - Company Name (Pending)',
                'verbose_name_plural': 'Substitutions - Company Name (Pending)',
            },
        ),
        migrations.CreateModel(
            name='SubCompanyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=40, unique=True)),
                ('substitution', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': 'Substitution - Company Type',
                'verbose_name_plural': 'Substitutions - Company Type',
            },
        ),
        migrations.CreateModel(
            name='SubCompanyTypePend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=40, unique=True)),
                ('substitution', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': 'Substitution - Company Type (Pending)',
                'verbose_name_plural': 'Substitutions - Company Type (Pending)',
            },
        ),
        migrations.CreateModel(
            name='SubDescriptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=210, unique=True)),
                ('substitution', models.CharField(max_length=210)),
            ],
            options={
                'verbose_name': 'Substitution - Descriptor',
                'verbose_name_plural': 'Substitutions - Descriptor',
            },
        ),
        migrations.CreateModel(
            name='SubDescriptorPend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=210, unique=True)),
                ('substitution', models.CharField(max_length=210)),
            ],
            options={
                'verbose_name': 'Substitution - Descriptor (Pending)',
                'verbose_name_plural': 'Substitutions - Descriptor (Pending)',
            },
        ),
        migrations.CreateModel(
            name='SubIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=240, unique=True)),
                ('substitution', models.CharField(max_length=240)),
            ],
            options={
                'verbose_name': 'Substitution - Ingredient',
                'verbose_name_plural': 'Substitutions - Ingredient',
            },
        ),
        migrations.CreateModel(
            name='SubIngredientPend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=240, unique=True)),
                ('substitution', models.CharField(max_length=240)),
            ],
            options={
                'verbose_name': 'Substitution - Ingredient (Pending)',
                'verbose_name_plural': 'Substitutions - Ingredient (Pending)',
            },
        ),
        migrations.CreateModel(
            name='SubPharmaceuticalStd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=40, unique=True)),
                ('substitution', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': 'Substitution - Pharmaceutical Standard',
                'verbose_name_plural': 'Substitutions - Pharmaceutical Standard',
            },
        ),
        migrations.CreateModel(
            name='SubPharmaceuticalStdPend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=40, unique=True)),
                ('substitution', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': 'Substitution - Pharmaceutical Standard (Pending)',
                'verbose_name_plural': 'Substitutions - Pharmaceutical Standard (Pending)',
            },
        ),
        migrations.CreateModel(
            name='SubProductCategorization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=80, unique=True)),
                ('substitution', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': 'Substitution - Categorization Product',
                'verbose_name_plural': 'Substitutions - Categorization Product',
            },
        ),
        migrations.CreateModel(
            name='SubProductCategorizationPend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=80, unique=True)),
                ('substitution', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': 'Substitution - Product Categorization (Pending)',
                'verbose_name_plural': 'Substitutions - Product Categorization (Pending)',
            },
        ),
        migrations.CreateModel(
            name='SubRouteOfAdministration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=40, unique=True)),
                ('substitution', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': 'Substitution - Route of Administration',
                'verbose_name_plural': 'Substitutions - Route of Administration',
            },
        ),
        migrations.CreateModel(
            name='SubRouteOfAdministrationPend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=40, unique=True)),
                ('substitution', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': 'Substitution - Route of Administration (Pending)',
                'verbose_name_plural': 'Substitutions - Route of Administration (Pending)',
            },
        ),
        migrations.CreateModel(
            name='SubStreetName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=80, unique=True)),
                ('substitution', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': 'Substitution - Street Name',
                'verbose_name_plural': 'Substitutions - Street Name',
            },
        ),
        migrations.CreateModel(
            name='SubStreetNamePend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=80, unique=True)),
                ('substitution', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': 'Substitution - Street Name (Pending)',
                'verbose_name_plural': 'Substitutions - Street Name (Pending)',
            },
        ),
        migrations.CreateModel(
            name='SubSuiteNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=20, unique=True)),
                ('substitution', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Substitution - Suite Number',
                'verbose_name_plural': 'Substitutions - Suite Number',
            },
        ),
        migrations.CreateModel(
            name='SubSuiteNumberPend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=20, unique=True)),
                ('substitution', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Substitution - Suite (Pending)',
                'verbose_name_plural': 'Substitutions - Suite (Pending)',
            },
        ),
        migrations.CreateModel(
            name='SubUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=40, unique=True)),
                ('substitution', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': 'Substitution - Unit',
                'verbose_name_plural': 'Substitutions - Unit',
            },
        ),
        migrations.CreateModel(
            name='SubUnitPend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=40, unique=True)),
                ('substitution', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': 'Substitution - Unit (Pending)',
                'verbose_name_plural': 'Substitutions - Unit (Pending)',
            },
        ),
        migrations.CreateModel(
            name='SubUPC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=12, unique=True)),
                ('substitution', models.CharField(max_length=12)),
            ],
            options={
                'verbose_name': 'Substitution - UPC',
                'verbose_name_plural': 'Substitutions - UPC',
            },
        ),
        migrations.CreateModel(
            name='SubUPCPend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(max_length=12, unique=True)),
                ('substitution', models.CharField(max_length=12)),
            ],
            options={
                'verbose_name': 'Substitution - UPC (Pending)',
                'verbose_name_plural': 'Substitutions - UPC (Pending)',
            },
        ),
        migrations.AlterModelOptions(
            name='subahfs',
            options={'verbose_name': 'Substitution - AHFS', 'verbose_name_plural': 'Substitutions - AHFS'},
        ),
        migrations.AlterModelOptions(
            name='subahfspend',
            options={
                'verbose_name': 'Substitution - AHFS (Pending)',
                'verbose_name_plural': 'Substitutions - AHFS (Pending)',
            },
        ),
    ]
