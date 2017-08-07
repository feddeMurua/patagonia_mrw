# -*- coding: utf-8 -*-
import django_filters
from .models import *


class PersonaListFilter(django_filters.FilterSet):
    class Meta:
        model = PersonaFisica
        fields = ['dni']
        order_by = ['dni']
