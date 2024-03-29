"""
To understand why this file is here, please read:

http://cookiecutter-django.readthedocs.io/en/latest/faq.html#why-is-there-a-django-contrib-sites-directory-in-cookiecutter-django
"""
# pylint: disable=missing-class-docstring
from django.conf import settings
from django.db import migrations


def update_site_forward(apps, schema_editor):  # pylint: disable=unused-argument
    """Set site domain and name."""
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        id=settings.SITE_ID,
        defaults={
            'domain': 'studybuffalo.com',
            'name': 'Study Buffalo',
        },
    )


def update_site_backward(apps, schema_editor):  # pylint: disable=unused-argument
    """Revert site domain and name to default."""
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        id=settings.SITE_ID, defaults={'domain': 'example.com', 'name': 'example.com'}
    )


class Migration(migrations.Migration):

    dependencies = [('sites', '0002_alter_domain_unique')]

    operations = [migrations.RunPython(update_site_forward, update_site_backward)]
