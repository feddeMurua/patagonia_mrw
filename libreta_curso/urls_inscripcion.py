from django.conf.urls import url
from django_filters.views import FilterView
from .filters import InscripcionListFilter
from .views import (
    ListaInscripcion,
    DetalleInscripcion,
    AltaInscripcion,
    BajaInscripcion,
    ModificacionInscripcion
)

urlpatterns = [

    url(r'^$', ListaInscripcion.as_view(), name='lista_inscripciones'),
    url(r'^(?P<pk>\d+)$', DetalleInscripcion.as_view(), name='detalle_inscripcion'),
    url(r'^nueva$', AltaInscripcion.as_view(), name='nueva_inscripcion'),
    url(r'^borrar/(?P<pk>\d+)$', BajaInscripcion.as_view(), name='borrar_inscripcion'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionInscripcion.as_view(), name='modificar_inscripcion'),
    url(r'^buscar/$', FilterView.as_view(filterset_class=InscripcionListFilter,
        template_name='inscripcion/inscripcion_search.html'), name='buscar_inscripcion'),
]
