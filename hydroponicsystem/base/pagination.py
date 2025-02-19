from rest_framework.pagination import PageNumberPagination


class HydroponicSystemPagination(PageNumberPagination):
    """3 elements per page."""
    page_size = 3