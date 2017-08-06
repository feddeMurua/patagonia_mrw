# -*- coding: utf-8 -*-
import django_filters
from .models import *


class AnalisisListFilter(django_filters.FilterSet):

    class Meta:
        model = Analisis
        fields = ['fecha']
        order_by = ['fecha']

