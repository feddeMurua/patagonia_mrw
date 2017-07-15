from django.conf.urls import url
from django_filters.views import FilterView
from .filters import ExamenListFilter

from .views import (
    ListaExamen,
    DetalleExamen,
    AltaExamen,
    BajaExamen,
)

urlpatterns = [

    url(r'^$', ListaExamen.as_view(), name='lista_examenes'),
    url(r'^(?P<pk>\d+)$', DetalleExamen.as_view(), name='detalle_examen'),
    url(r'^nuevo$', AltaExamen.as_view(), name='nuevo_examen'),
    url(r'^borrar/(?P<pk>\d+)$', BajaExamen.as_view(), name='borrar_examen'),
    url(r'^buscar/$', FilterView.as_view(filterset_class=ExamenListFilter,
        template_name='examen/examen_search.html'), name='buscar_examen'),


]
