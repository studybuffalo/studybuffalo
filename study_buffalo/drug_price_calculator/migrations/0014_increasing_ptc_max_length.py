from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drug_price_calculator', '0013_increasing_max_lengths'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ptc',
            name='ptc_1_text',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='PTC level 1 description'),
        ),
        migrations.AlterField(
            model_name='ptc',
            name='ptc_2_text',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='PTC level 2 description'),
        ),
        migrations.AlterField(
            model_name='ptc',
            name='ptc_3_text',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='PTC level 3 description'),
        ),
        migrations.AlterField(
            model_name='ptc',
            name='ptc_4_text',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='PTC level 4 description'),
        ),
    ]
