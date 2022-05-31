"""Validators for the HC DPD app API."""
from rest_framework.serializers import ValidationError


class AscendingDrugCode:  # pylint: disable=too-few-public-methods
    """Validates that drug codes are in ascending order."""
    def __call__(self, value):
        last_drug_code = 0

        for file_name, values in dict(value).items():
            for row in values:
                drug_code = dict(row)['drug_code']

                if drug_code < last_drug_code:
                    message = f'{file_name} error: drug codes must be in ascending order to calculate checksum'
                    raise ValidationError(message)

                last_drug_code = drug_code
