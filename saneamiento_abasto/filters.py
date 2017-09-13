# -*- coding: utf-8 -*-
import django_filters
from .models import *


class AbastecedorListFilter(django_filters.FilterSet):
    class Meta:
        model = Abastecedor
        fields = ['empresa']
        order_by = ['empresa']


class ReinspeccionListFilter(django_filters.FilterSet):
    class Meta:
        model = Reinspeccion
        fields = ['fecha']
        order_by = ['fecha']


class VehiculoListFilter(django_filters.FilterSet):
    class Meta:
        model = Vehiculo
        fields = ['dominio']
        order_by = ['dominio']


class DesinfeccionListFilter(django_filters.FilterSet):
    class Meta:
        model = Desinfeccion
        fields = ['vehiculo']
        order_by = ['vehiculo']
