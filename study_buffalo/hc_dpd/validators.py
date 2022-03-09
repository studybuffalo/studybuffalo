"""Validators to support the HC DPD app."""
from django.core.exceptions import ValidationError


def validate_checksum_start(start, step):
    """Confirms start value is a multiple of the step.

        This validation ensures that start values are consistent and
        minimizes the number of checksums required.
    """
    if start % step != 0:
        examples = [0 * step, 1 * step, 2 * step]
        message = f'Start values must be multiples of the step ({step}), such as {", ".join(examples)}, etc.'

        raise ValidationError(
            message,
            params={'start': start, 'step': step}
        )
