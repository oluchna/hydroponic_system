from rest_framework.pagination import PageNumberPagination


class HydroponicSystemPagination(PageNumberPagination):
    page_size = 3