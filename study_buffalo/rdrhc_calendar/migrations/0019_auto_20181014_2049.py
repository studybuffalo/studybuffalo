# pylint: disable=missing-module-docstring, missing-class-docstring
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0018_auto_20171118_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendaruser',
            name='sb_user',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='calendar_user',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
