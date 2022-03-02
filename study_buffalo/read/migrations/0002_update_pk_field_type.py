"""Update primary key field type."""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentpublication',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='htmlpublication',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
