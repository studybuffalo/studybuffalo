# pylint: disable=missing-module-docstring, missing-class-docstring
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rdrhc_calendar', '0019_auto_20181014_2049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calendaruser',
            options={
                'permissions': (
                    ('can_view', 'Can view the RDRHC Calendar settings view'),
                    ('access_api', 'Can access all API endpoints'),
                ),
                'verbose_name': 'RDRHC Calendar User',
                'verbose_name_plural': 'RDRHC Calendar Users',
            },
        ),
        migrations.AlterField(
            model_name='shift',
            name='sb_user',
            field=models.ForeignKey(
                help_text='The user this shift applies to',
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
