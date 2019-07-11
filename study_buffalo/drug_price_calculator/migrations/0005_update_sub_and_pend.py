from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('drug_price_calculator', '0004_new_model_structure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendbsrf',
            name='brand_name',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='pendbsrf',
            name='dosage_form',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='pendbsrf',
            name='route',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='pendbsrf',
            name='strength',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pendgeneric',
            name='correction',
            field=models.CharField(blank=True, max_length=450, null=True),
        ),
        migrations.AlterField(
            model_name='pendmanufacturer',
            name='correction',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='subsbsrf',
            name='brand_name',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='subsbsrf',
            name='dosage_form',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='subsbsrf',
            name='route',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='subsbsrf',
            name='strength',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='subsgeneric',
            name='correction',
            field=models.CharField(blank=True, max_length=450, null=True),
        ),
        migrations.AlterField(
            model_name='subsmanufacturer',
            name='correction',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='subsunit',
            name='correction',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
