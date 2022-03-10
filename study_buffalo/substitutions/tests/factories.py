"""Factories for testing the Substitutions app."""
import factory

from substitutions import models


class AppsFactory(factory.django.DjangoModelFactory):
    """Factory to generate an Apps instance."""
    app_name = 'hc_dpd'
    model_pending = 'SubBrandPending'
    model_sub = 'SubBrand'

    class Meta:
        model = models.Apps
        django_get_or_create = ('app_name', 'model_pending', 'model_sub')


class ModelFieldsFactory(factory.django.DjangoModelFactory):
    """Factory to generate a ModelFields."""
    app = factory.SubFactory(AppsFactory)
    field_name = 'original'
    field_type = 'o'
    dictionary_check = False
    google_check = False

    class Meta:
        model = models.ModelFields
        django_get_or_create = ('app', 'field_name')
