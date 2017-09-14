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
        fields = ['fecha']
        order_by = ['fecha']


class TsaListFilter(django_filters.FilterSet):
    class Meta:
        model = Tsa
        fields = ['persona']
        order_by = ['persona']


class TppListFilter(django_filters.FilterSet):
    class Meta:
        model = Tsa
        fields = ['persona']
        order_by = ['persona']


class DesinfeccionListFilter(django_filters.FilterSet):
    class Meta:
        model = Desinfeccion
        fields = ['transporte']
        order_by = ['transporte']
