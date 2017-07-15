from django.conf.urls import url
from django_filters.views import FilterView
from .filters import PersonaListFilter
from .views import (
    ListaPersona,
    DetallePersona,
    AltaPersona,
    BajaPersona,
    ModificacionPersona
)

urlpatterns = [

    url(r'^$', ListaPersona.as_view(), name='lista_personas'),
    url(r'^(?P<pk>\d+)$', DetallePersona.as_view(), name='detalle_persona'),
    url(r'^nueva$', AltaPersona.as_view(), name='nueva_persona'),
    url(r'^borrar/(?P<pk>\d+)$', BajaPersona.as_view(), name='borrar_persona'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionPersona.as_view(), name='modificar_persona'),
    url(r'^buscar/$', FilterView.as_view(filterset_class=PersonaListFilter,
        template_name='persona/persona_search.html'), name='buscar_persona'),
]
