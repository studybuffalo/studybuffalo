"""Setting up test configuration."""
import pytest

from dictionary.tests import factories as dictionary_factories
from rdrhc_calendar.tests import factories as rdrhc_calendar_factories
from users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):  # pylint: disable=redefined-outer-name
    """Fixture to support media stroage in tests."""
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user():
    """Fixture to create a User instance."""
    return UserFactory()


@pytest.fixture
def calendar_user():
    """Fixture to create an RDRHC Calendar User instance."""
    return rdrhc_calendar_factories.CalendarUserFactory()


@pytest.fixture
def shift_code():
    """Fixture to create a Shift Code instance."""
    return rdrhc_calendar_factories.ShiftCodeFactory()


@pytest.fixture
def shift():
    """Fixture to create a Shift instance."""
    return rdrhc_calendar_factories.ShiftFactory()


@pytest.fixture
def missing_shift_code():
    """Fixture to create a Missing Shift Code instance."""
    return rdrhc_calendar_factories.MissingShiftCodeFactory()


@pytest.fixture
def dictionary_word():
    """Fixture to create a Word instance."""
    return dictionary_factories.WordFactory()


@pytest.fixture
def dictionary_word_pending():
    """Fixture to create a WordPending instance."""
    return dictionary_factories.WordPendingFactory()


@pytest.fixture
def dictionary_excluded_word():
    """Fixture to create an ExcludedWord instance."""
    return dictionary_factories.ExcludedWordFactory()
