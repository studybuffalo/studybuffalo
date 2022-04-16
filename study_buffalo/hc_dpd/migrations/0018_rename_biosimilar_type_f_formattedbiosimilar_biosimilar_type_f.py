# pylint: disable=missing-module-docstring, missing-class-docstring
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hc_dpd', '0017_rename_biosimilar_type_f_originalbiosimilar_biosimilar_type_f'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formattedbiosimilar',
            old_name='biosimilar_type_F',
            new_name='biosimilar_type_f',
        ),
    ]
