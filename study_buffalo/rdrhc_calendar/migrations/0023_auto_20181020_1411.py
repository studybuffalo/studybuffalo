# pylint: disable=missing-module-docstring, missing-class-docstring
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0022_auto_20181020_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='sb_user',
            field=models.ForeignKey(
                help_text='The user this shift applies to',
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name='SB user',
            ),
        ),
    ]
