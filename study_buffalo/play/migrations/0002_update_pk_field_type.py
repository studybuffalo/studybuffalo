"""Update primary key field type."""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0001_squashed_0008_auto_20170828_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='playpage',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
