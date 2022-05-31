
"""Admin settings for the Health Canda Drug Product Database app."""
from .core import DPDAdmin
from .formatted import (
    FormattedActiveIngredientAdmin, FormattedBiosimilarAdmin,
    FormattedCompanyAdmin, FormattedDrugProductAdmin,
    FormattedFormAdmin, FormattedInactiveProductAdmin,
    FormattedPackagingAdmin, FormattedPharmaceuticalStandardAdmin,
    FormattedRouteAdmin, FormattedScheduleAdmin, FormattedStatusAdmin,
    FormattedTherapeuticClassAdmin, FormattedVeterinarySpeciesAdmin,
)
from .original import (
    OriginalActiveIngredientAdmin, OriginalBiosimilarAdmin,
    OriginalCompanyAdmin, OriginalDrugProductAdmin,
    OriginalFormAdmin, OriginalInactiveProductAdmin,
    OriginalPackagingAdmin, OriginalPharmaceuticalStandardAdmin,
    OriginalRouteAdmin, OriginalScheduleAdmin, OriginalStatusAdmin,
    OriginalTherapeuticClassAdmin, OriginalVeterinarySpeciesAdmin,
)
from .substitutions import (
    SubBrandAdmin, SubBrandPendAdmin, SubCompanyNameAdmin,
    SubCompanyNamePendAdmin, SubDescriptorAdmin, SubDescriptorPendAdmin,
    SubIngredientAdmin, SubIngredientPendAdmin, SubPharmaceuticalStdAdmin,
    SubPharmaceuticalStdPendAdmin, SubProductCategorizationAdmin,
    SubProductCategorizationPendAdmin, SubRouteOfAdministrationAdmin,
    SubRouteOfAdministrationPendAdmin, SubStreetNameAdmin,
    SubStreetNamePendAdmin, SubSuiteNumberAdmin, SubSuiteNumberPendAdmin,
    SubUnitAdmin, SubUnitPendAdmin,
)
