# -*- coding: utf-8 -*-
import django_filters
from .models import *


class DetalleMovimientoListFilter(django_filters.FilterSet):

    class Meta:
        model = DetalleMovimiento
        fields = ['movimiento']
        order_by = ['movimiento']
