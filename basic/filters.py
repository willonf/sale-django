from django.db.models import Q
from django_filters import filterset
from django_filters.widgets import BooleanWidget

from basic import models


# TODO: Filtros
# Filtro in
class NumberInFilter(filterset.BaseInFilter, filterset.NumberFilter):
    pass


class CharInFilter(filterset.BaseInFilter, filterset.CharFilter):
    pass


# Filtro por range
class NumberRangeFilter(filterset.BaseRangeFilter, filterset.NumberFilter):
    pass


class ZoneFilter(filterset.FilterSet):
    name = filterset.CharFilter(lookup_expr='icontains')
    active = filterset.BooleanFilter(widget=BooleanWidget)


class EmployeeFilter(filterset.FilterSet):
    name_or_department = filterset.CharFilter(method='')
    start_salary = filterset.NumberFilter(field_name='salary', lookup_expr='gte')
    end_salary = filterset.NumberFilter(field_name='salary', lookup_expr='lte')
    salary_range = NumberRangeFilter(field_name='salary', lookup_expr='range')
    salary_in = NumberInFilter(field_name='salary', lookup_expr='range')
    gender_in = CharInFilter(field_name='gender', lookup_expr='in')

    @staticmethod
    def filter_name_or_department(self, queryset, name, value):
        # queryset: queryset do viewset
        # name: nome do filtro
        # value: dado oriundo da requisição
        return queryset.filter(Q(name__icontains=value) | Q(department__name__icontains=value))

    class Meta:
        model = models.Employee
        fields = ['start_salary', 'end_salary', 'salary_range']
