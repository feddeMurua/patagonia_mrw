import django_filters
from .models import LibretaSanitaria


class LibretaListFilter(django_filters.FilterSet):

  class Meta:
    model = LibretaSanitaria
    fields = ['curso','fecha']
    order_by = ['pk']
