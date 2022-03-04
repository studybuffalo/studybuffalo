"""Update primary key field type."""
# pylint: disable=missing-class-docstring
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0002_auto_20171003_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
