from django_filters import rest_framework as filters

from .models import HydroponicSystem


class HydroponicSystemFilter(filters.FilterSet):
    """Definition of the type of filters on the fields."""
    system_name = filters.CharFilter(lookup_expr='icontains')
    volume = filters.RangeFilter()
    activation_dt = filters.DateTimeFromToRangeFilter()
    num_of_chambers = filters.RangeFilter()

    class Meta:
        model = HydroponicSystem
        fields = ['system_name', 'volume', 'activation_dt', 'num_of_chambers']