# -*- coding: utf-8 -*-
import django_filters
from .models import *


class AnalisisListFilter(django_filters.FilterSet):

    class Meta:
        model = Analisis
        fields = ['fecha']
        order_by = ['fecha']


class SolicitudListFilter(django_filters.FilterSet):

    class Meta:
        model = SolicitudCriaderoCerdos
        fields = ['interesado']
        order_by = ['interesado']


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


class ControlListFilter(django_filters.FilterSet):

    class Meta:
        model = ControlAntirrabico
        fields = ['fecha_suceso']
        order_by = ['fecha_suceso']


class VisitaListFilter(django_filters.FilterSet):

    class Meta:
        model = Visita
        fields = ['fecha_visita']
        order_by = ['fecha_visita']


class RetiroEntregaListFilter(django_filters.FilterSet):

    class Meta:
        model = RetiroEntregaAnimal
        fields = ['interesado']
        order_by = ['interesado']
