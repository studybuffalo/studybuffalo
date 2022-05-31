# pylint: disable=missing-module-docstring, missing-class-docstring, line-too-long
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0014_update_models_for_api'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormattedBiosimilar',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'biosimilar_code',
                    models.PositiveIntegerField(
                        blank=True,
                        help_text='The formatted version of BIOSIMILAR_CODE.',
                        null=True,
                    ),
                ),
                (
                    'biosimilar_type',
                    models.CharField(
                        blank=True,
                        help_text='The formatted version of BIOSIMILAR_TYPE.',
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    'biosimilar_type_f',
                    models.CharField(
                        blank=True,
                        help_text='The formatted version of BIOSIMILAR_TYPE_F.',
                        max_length=20,
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.RenameField(
            model_name='dpd',
            old_name='original_biosimilars_modified',
            new_name='original_biosimilar_modified',
        ),
        migrations.RenameField(
            model_name='originalbiosimilar',
            old_name='biosimilar_type_F',
            new_name='biosimilar_type_f',
        ),
        migrations.AlterField(
            model_name='dpdchecksum',
            name='checksum',
            field=models.CharField(blank=True, help_text='The checksum value for the specified items.', max_length=10),
        ),
        migrations.AlterField(
            model_name='formattedactiveingredient',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='formatted_active_ingredients', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='formattedcompany',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='formatted_companies', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='formatteddrugproduct',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='formatted_drug_products', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='formattedform',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='formatted_forms', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='formattedinactiveproduct',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='formatted_inactive_products', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='formattedpackaging',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='formatted_packaging', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='formattedpharmaceuticalstandard',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='formatted_pharmaceutical_standards', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='formattedroute',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='formatted_routes', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='formattedschedule',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='formatted_schedules', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='formattedstatus',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='formatted_statuses', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='formattedtherapeuticclass',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='formatted_therapeutic_classes', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='formattedveterinaryspecies',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='formatted_veterinary_species', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalactiveingredient',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_active_ingredients', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalbiosimilar',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_biosimilars', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalcompany',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_companies', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originaldrugproduct',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_drug_products', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalform',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_forms', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalinactiveproduct',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_inactive_products', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalpackaging',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_packaging', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalpharmaceuticalstandard',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_pharmaceutical_standards', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalroute',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_routes', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalschedule',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_schedules', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalstatus',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_statuses', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originaltherapeuticclass',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_therapeutic_classes', to='hc_dpd.dpd'),
        ),
        migrations.AlterField(
            model_name='originalveterinaryspecies',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='original_veterinary_species', to='hc_dpd.dpd'),
        ),
        migrations.DeleteModel(
            name='FormattedBiosimilars',
        ),
        migrations.AddField(
            model_name='formattedbiosimilar',
            name='drug_code',
            field=models.ForeignKey(help_text='The drug code reference for this item.', on_delete=django.db.models.deletion.CASCADE, related_name='formatted_biosimilars', to='hc_dpd.dpd'),
        ),
    ]
