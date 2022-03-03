# pylint: disable=missing-module-docstring, missing-class-docstring
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rdrhc_calendar', '0013_auto_20171016_1915'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shift',
            old_name='user',
            new_name='sb_user',
        ),
        migrations.RenameField(
            model_name='shiftcode',
            old_name='user',
            new_name='sb_user',
        ),
        migrations.AlterUniqueTogether(
            name='shiftcode',
            unique_together=set([('code', 'sb_user', 'role')]),
        ),
    ]
