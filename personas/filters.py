# -*- coding: utf-8 -*-
import django_filters
from .models import *


class PersonaListFilter(django_filters.FilterSet):
    class Meta:
        model = PersonaFisica
        fields = ['dni']
        order_by = ['dni']


class PersonaJuridicaListFilter(django_filters.FilterSet):
    class Meta:
        model = PersonaJuridica
        fields = ['cuit']
        order_by = ['cuit']


class PersonalPropioListFilter(django_filters.FilterSet):
    class Meta:
        model = PersonalPropio
        fields = ['rol_actuante']
        order_by = ['rol_actuante']