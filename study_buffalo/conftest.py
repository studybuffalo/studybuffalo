"""Setting up test configuration."""
import pytest

from dictionary.tests import factories as dictionary_factories
from hc_dpd.tests import factories as hc_dpd_factories
from play.tests import factories as play_factories
from rdrhc_calendar.tests import factories as rdrhc_calendar_factories
from read.tests import factories as read_factories
from study.tests import factories as study_factories
from substitutions.tests import factories as substitutions_factories
from updates.tests import factories as updates_factories
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


@pytest.fixture
def hc_dpd_dpd():
    """Fixture to create DPD instance."""
    return hc_dpd_factories.DPDFactory()


@pytest.fixture
def hc_dpd_original_active_ingredient():
    """Fixture to create OriginalActiveIngredient instance."""
    return hc_dpd_factories.OriginalActiveIngredientFactory()


@pytest.fixture
def hc_dpd_original_biosimilar():
    """Fixture to create OriginalBiosimilar instance."""
    return hc_dpd_factories.OriginalBiosimilarFactory()


@pytest.fixture
def hc_dpd_original_company():
    """Fixture to create OriginalCompany instance."""
    return hc_dpd_factories.OriginalCompanyFactory()


@pytest.fixture
def hc_dpd_original_drug_product():
    """Fixture to create OriginalDrugProduct instance."""
    return hc_dpd_factories.OriginalDrugProductFactory()


@pytest.fixture
def hc_dpd_original_form():
    """Fixture to create OriginalForm instance."""
    return hc_dpd_factories.OriginalFormFactory()


@pytest.fixture
def hc_dpd_original_inactive_product():
    """Fixture to create OriginalInactiveProduct instance."""
    return hc_dpd_factories.OriginalInactiveProductFactory()


@pytest.fixture
def hc_dpd_original_packaging():
    """Fixture to create OriginalPackaging instance."""
    return hc_dpd_factories.OriginalPackagingFactory()


@pytest.fixture
def hc_dpd_original_pharmaceutical_standard():
    """Fixture to create OriginalPharmaceuticalStandard instance."""
    return hc_dpd_factories.OriginalPharmaceuticalStandardFactory()


@pytest.fixture
def hc_dpd_original_route():
    """Fixture to create OriginalRoute instance."""
    return hc_dpd_factories.OriginalRouteFactory()


@pytest.fixture
def hc_dpd_original_schedule():
    """Fixture to create Originalschedule instance."""
    return hc_dpd_factories.OriginalScheduleFactory()


@pytest.fixture
def hc_dpd_original_status():
    """Fixture to create OriginalStatus instance."""
    return hc_dpd_factories.OriginalStatusFactory()


@pytest.fixture
def hc_dpd_original_therapeutic_class():
    """Fixture to create OriginalTherapeuticClass instance."""
    return hc_dpd_factories.OriginalTherapeuticClassFactory()


@pytest.fixture
def hc_dpd_original_veterinary_species():
    """Fixture to create OriginalVeterinarySpecies instance."""
    return hc_dpd_factories.OriginalVeterinarySpeciesFactory()


@pytest.fixture
def hc_dpd_two_original_active_ingredient():
    """Fixture to create two OriginalActiveIngredient instances."""
    return [
        hc_dpd_factories.OriginalActiveIngredientFactory(),
        hc_dpd_factories.OriginalActiveIngredientFactory(),
    ]


@pytest.fixture
def hc_dpd_checksum_active_ingredient():
    """Fixture to create DPDChecksum instance with Active Ingredient data."""
    return hc_dpd_factories.DPDChecksumActiveIngredientFactory()


@pytest.fixture
def hc_dpd_sub_brand():
    """Fixture to create SubBrand instance."""
    return hc_dpd_factories.SubBrandFactory()


@pytest.fixture
def hc_dpd_sub_brand_pend():
    """Fixture to create SubBrandPend instance."""
    return hc_dpd_factories.SubBrandPendFactory()


@pytest.fixture
def play_page():
    """Fixture to create a PlayPage instance."""
    return play_factories.PlayPageFactory()


@pytest.fixture
def play_image():
    """Fixture to create a PlayImage instance."""
    return play_factories.PlayImageFactory()


@pytest.fixture
def play_image_large():
    """Fixture to create a PlayImage instance with large image."""
    return play_factories.PlayImageLargeFactory()


@pytest.fixture
def play_audio():
    """Fixture to create a PlayAudio instance."""
    return play_factories.PlayAudioFactory()


@pytest.fixture
def read_publication():
    """Fixture to create a Publication instance."""
    return read_factories.PublicationFactory()


@pytest.fixture
def read_html_publication():
    """Fixture to create an HTMLPublication instance."""
    return read_factories.HTMLPublicationFactory()


@pytest.fixture
def read_document_publication():
    """Fixture to create a DocumentPublication instance."""
    return read_factories.DocumentPublicationFactory()


@pytest.fixture
def study_guide():
    """Fixture to create a Guide instance."""
    return study_factories.GuideFactory()


@pytest.fixture
def study_bounty():
    """Fixture to create a Bounty instance."""
    return study_factories.BountyFactory()


@pytest.fixture
def study_bounty_assignment():
    """Fixture to create a BountyAssignment instance."""
    return study_factories.BountyAssignment()


@pytest.fixture
def study_html_guide():
    """Fixture to create a HTMLGuide instance."""
    return study_factories.HTMLGuideFactory()


@pytest.fixture
def study_document_guide():
    """Fixture to create a DocumentGuide instance."""
    return study_factories.DocumentGuideFactory()


@pytest.fixture
def substitutions_apps():
    """Fixture to create an Apps instance."""
    return substitutions_factories.AppsFactory()


@pytest.fixture
def substitutions_model_fields():
    """Fixture to create a ModelFields instance."""
    return substitutions_factories.ModelFieldsFactory()


@pytest.fixture
def updates_update():
    """Fixture to create an Update instance."""
    return updates_factories.UpdateFactory()
