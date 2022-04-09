# pylint: disable=missing-module-docstring, missing-class-docstring
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('hc_dpd', '0015_add_related_names'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FormattedBiosimilars',
            new_name='FormattedBiosimilar',
        ),
    ]
