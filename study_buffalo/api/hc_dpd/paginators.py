"""Paginators for the HC DPD API."""
from rest_framework import pagination


class ChecksumPagination(pagination.PageNumberPagination):
    """Pagination settings for the ChecksumList view."""
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 1000
