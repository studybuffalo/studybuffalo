# pylint: disable=missing-module-docstring, missing-class-docstring
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0016_alter_dpdchecksum_checksum'),
    ]

    operations = [
        migrations.RenameField(
            model_name='originalbiosimilar',
            old_name='biosimilar_type_F',
            new_name='biosimilar_type_f',
        ),
    ]
