# pylint: disable=missing-module-docstring, missing-class-docstring
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0021_auto_20181020_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiftcode',
            name='sb_user',
            field=models.ForeignKey(
                blank=True,
                help_text='Which user this shift code applies to (leave blank for a default entry)',
                null=True, on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name='SB user',
            ),
        ),
    ]
