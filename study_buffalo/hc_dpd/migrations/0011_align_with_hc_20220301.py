# pylint: disable=missing-module-docstring, missing-class-docstring
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0010_update_pk_field_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dpd',
            name='origin_file',
        ),
        migrations.RemoveField(
            model_name='therapeuticclass',
            name='tc_ahfs',
        ),
        migrations.RemoveField(
            model_name='therapeuticclass',
            name='tc_ahfs_f',
        ),
        migrations.RemoveField(
            model_name='therapeuticclass',
            name='tc_ahfs_number',
        ),
        migrations.AlterField(
            model_name='activeingredient',
            name='active_ingredient_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='activeingredient',
            name='base',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='activeingredient',
            name='ingredient_f',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='address_billing_flag',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='address_mailing_flag',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='address_notification_flag',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='address_other',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='country_f',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='province_f',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='drugproduct',
            name='brand_name_f',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='drugproduct',
            name='class_f',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='drugproduct',
            name='descriptor',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='drugproduct',
            name='descriptor_f',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='drugproduct',
            name='drug_identification_number',
            field=models.CharField(blank=True, max_length=29, null=True),
        ),
        migrations.AlterField(
            model_name='drugproduct',
            name='pediatric_flag',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='form',
            name='pharmaceutical_form_f',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='inactiveproduct',
            name='drug_identification_number',
            field=models.CharField(blank=True, max_length=29, null=True),
        ),
        migrations.AlterField(
            model_name='packaging',
            name='package_size',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='packaging',
            name='product_information',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='route_of_administration',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='route_of_administration_f',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule_f',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='current_status_flag',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='lot_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='therapeuticclass',
            name='tc_atc_f',
            field=models.CharField(blank=True, max_length=240, null=True),
        ),
        migrations.AlterField(
            model_name='veterinaryspecies',
            name='vet_species_f',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
    ]
