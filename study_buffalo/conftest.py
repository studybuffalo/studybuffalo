"""Setting up test configuration."""
import pytest

from users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir): # pylint: disable=redefined-outer-name
    settings.MEDIA_ROOT = tmpdir.strpath

@pytest.fixture
def user():
    return UserFactory()
