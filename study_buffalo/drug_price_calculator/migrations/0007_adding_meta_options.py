from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('drug_price_calculator', '0006_auto_20190711_0742'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clients',
            options={'verbose_name_plural': 'clients'},
        ),
        migrations.AlterModelOptions(
            name='coveragecriteria',
            options={'verbose_name_plural': 'coverage criteria'},
        ),
        migrations.AlterModelOptions(
            name='pendbsrf',
            options={'verbose_name': 'Substitution - BSRF (Pending)', 'verbose_name_plural': 'Substitutions - BSRF (Pending)'},
        ),
        migrations.AlterModelOptions(
            name='pendgeneric',
            options={'verbose_name': 'Substitution - Generic (Pending)', 'verbose_name_plural': 'Substitutions - Generic (Pending)'},
        ),
        migrations.AlterModelOptions(
            name='pendmanufacturer',
            options={'verbose_name': 'Substitution - Manufactuer (Pending)', 'verbose_name_plural': 'Substitutions - Manufactuer (Pending)'},
        ),
        migrations.AlterModelOptions(
            name='ptc',
            options={'verbose_name': 'Pharmacologic-Therapeutic Classification', 'verbose_name_plural': 'Pharmacologic-Therapeutic Classifications'},
        ),
        migrations.AlterModelOptions(
            name='subsbsrf',
            options={'verbose_name': 'Substitution - BSRF', 'verbose_name_plural': 'Substitutions - BSRF'},
        ),
        migrations.AlterModelOptions(
            name='subsgeneric',
            options={'verbose_name': 'Substitution - Generic', 'verbose_name_plural': 'Substitutions - Generic'},
        ),
        migrations.AlterModelOptions(
            name='subsmanufacturer',
            options={'verbose_name': 'Substitution - Manufacturer', 'verbose_name_plural': 'Substitutions - Manufacturer'},
        ),
        migrations.AlterModelOptions(
            name='subsunit',
            options={'verbose_name': 'Substitution - Unit', 'verbose_name_plural': 'Substitutions - Unit'},
        ),
    ]
