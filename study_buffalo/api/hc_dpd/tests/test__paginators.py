"""Tests for the HC DPD API paginators."""
from api.hc_dpd import paginators


def test__checksum_pagination__settings():
    """Confirms settings for Checksum pagination."""
    paginator = paginators.ChecksumPagination

    assert paginator.page_size == 1000
    assert paginator.max_page_size == 1000
    assert paginator.page_size_query_param == 'page_size'
