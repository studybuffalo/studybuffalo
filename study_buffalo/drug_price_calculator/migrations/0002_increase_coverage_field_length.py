from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('drug_price_calculator', '0001_squashed_0009_auto_20170920_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coverage',
            name='coverage',
            field=models.CharField(max_length=60),
        ),
    ]
