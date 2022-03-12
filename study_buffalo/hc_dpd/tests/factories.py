"""Factories for testing the HC DPD app."""
import factory

from hc_dpd import models


class SubBrandFactory(factory.django.DjangoModelFactory):
    """Factory to generate a SubBrand instance."""
    original = 'Original Brand 1'
    substitution = 'Sub Brand 1'

    class Meta:
        model = models.SubBrand
        django_get_or_create = ('original', 'substitution')


class SubBrandPendFactory(factory.django.DjangoModelFactory):
    """Factory to generate a SubBrandPend instance."""
    original = 'Original Brand 1 Pending'
    substitution = 'Sub Brand 1 Pending'

    class Meta:
        model = models.SubBrandPend
        django_get_or_create = ('original', 'substitution')
