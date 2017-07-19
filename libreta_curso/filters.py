# -*- coding: utf-8 -*-
import django_filters
from .models import *


class LibretaListFilter(django_filters.FilterSet):

    class Meta:
        model = LibretaSanitaria
        fields = ['curso', 'fecha_examen_clinico']
        order_by = ['fecha_examen_clinico']


class CursoListFilter(django_filters.FilterSet):
    class Meta:
        model = Curso
        fields = ['cupo', 'horario', 'fecha_inicio']
        order_by = ['cupo']


class InscripcionListFilter(django_filters.FilterSet):
    class Meta:
        model = Inscripcion
        fields = ['persona']
        order_by = ['persona']
