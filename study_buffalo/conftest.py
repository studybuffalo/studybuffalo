"""Setting up test configuration."""
import pytest

from rest_framework.authtoken.models import Token

from rdrhc_calendar.tests import factories as rdrhc_calendar_factories
from users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir): # pylint: disable=redefined-outer-name
    settings.MEDIA_ROOT = tmpdir.strpath

@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def calendar_user():
    return rdrhc_calendar_factories.CalendarUserFactory()

@pytest.fixture
def shift_code():
    return rdrhc_calendar_factories.ShiftCodeFactory()

@pytest.fixture
def shift():
    return rdrhc_calendar_factories.ShiftFactory()

@pytest.fixture
def missing_shift_code():
    return rdrhc_calendar_factories.MissingShiftCodeFactory()

@pytest.fixture
def token():
    fixture_user = UserFactory()

    return Token.objects.create(user=fixture_user)
