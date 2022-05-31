"""General utility functions for API modules."""


def convert_serializer_errors(errors):
    """Converts serializer errors into standard error format."""
    try:
        non_field_errors = errors.pop('non_field_errors')
    except KeyError:
        non_field_errors = []

    return {
        'field': errors,
        'non_field': non_field_errors,
    }
