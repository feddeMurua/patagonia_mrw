# -*- coding: utf-8 -*-
import django_filters
from .models import *


class PatenteListFilter(django_filters.FilterSet):

    class Meta:
        model = Patente
        fields = ['fecha']
        order_by = ['fecha']

