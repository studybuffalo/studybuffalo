"""Factories to create working user and related models."""
import factory

from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    """Factory to create a User."""
    username = factory.Sequence(lambda n: f'user-{n}')
    email = factory.Sequence(lambda n: f'user-{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)
