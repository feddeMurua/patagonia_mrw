# -*- coding: utf-8 -*-
import django_filters
from .models import *


class AbastecedorListFilter(django_filters.FilterSet):
    class Meta:
        model = Abastecedor
        fields = ['persona']
        order_by = ['persona']


class ReinspeccionListFilter(django_filters.FilterSet):
    class Meta:
        model = Reinspeccion
        fields = ['abastecedor']
        order_by = ['abastecedor']
