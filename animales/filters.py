# -*- coding: utf-8 -*-
import django_filters
from .models import *


class AnalisisListFilter(django_filters.FilterSet):

    class Meta:
        model = Analisis
        fields = ['fecha']
        order_by = ['fecha']


class HabilitacionListFilter(django_filters.FilterSet):

    class Meta:
        model = HabilitacionCriaderoCerdos
        fields = ['fecha_disposicion']
        order_by = ['fecha_disposicion']


class EsterilizacionListFilter(django_filters.FilterSet):

    class Meta:
        model = Esterilizacion
        fields = ['turno']
        order_by = ['turno']


class PatenteListFilter(django_filters.FilterSet):

    class Meta:
        model = Patente
        fields = ['fecha']
        order_by = ['fecha']
