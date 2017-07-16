import django_filters
from .models import *


class LibretaListFilter(django_filters.FilterSet):

    class Meta:
        model = LibretaSanitaria
        fields = ['curso', 'fecha']
        order_by = ['fecha']


class PersonaListFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    apellido = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = PersonaFisica
        fields = ['nombre', 'apellido', 'dni']
        order_by = ['apellido']


class ExamenListFilter(django_filters.FilterSet):
    profesional = django_filters.CharFilter(lookup_expr='icontains')
    centro_atencion = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ExamenClinico
        fields = ['fecha', 'profesional', 'centro_atencion']
        order_by = ['fecha']


class CursoListFilter(django_filters.FilterSet):
    class Meta:
        model = Curso
        fields = ['cupo', 'horario']
        order_by = ['cupo']


class InscripcionListFilter(django_filters.FilterSet):
    class Meta:
        model = Inscripcion
        fields = ['curso']
        order_by = ['curso']
