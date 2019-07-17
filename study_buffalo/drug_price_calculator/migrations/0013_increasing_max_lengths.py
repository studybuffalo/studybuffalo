from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drug_price_calculator', '0012_increasing_strength_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug',
            name='brand_name',
            field=models.CharField(blank=True, help_text='The brand name or trade name', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='drug',
            name='dosage_form',
            field=models.CharField(blank=True, help_text='The dosage form', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='drug',
            name='manufacturer',
            field=models.CharField(blank=True, help_text='The drug manufacturer', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='drug',
            name='strength',
            field=models.CharField(blank=True, help_text='The strength(s) of the medications', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='pendbsrf',
            name='original',
            field=models.CharField(max_length=400, unique=True),
        ),
        migrations.AlterField(
            model_name='pendbsrf',
            name='strength',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='subsbsrf',
            name='original',
            field=models.CharField(max_length=400, unique=True),
        ),
        migrations.AlterField(
            model_name='subsbsrf',
            name='strength',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='subsmanufacturer',
            name='correction',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='subsmanufacturer',
            name='original',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
