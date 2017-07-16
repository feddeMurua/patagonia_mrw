from django.conf.urls import url
from .views import (
    ListaExamen,
    DetalleExamen,
    AltaExamen,
    BajaExamen,
)

urlpatterns = [
    url(r'^$', ListaExamen, name='lista_examenes'),
    url(r'^(?P<pk>\d+)$', DetalleExamen.as_view(), name='detalle_examen'),
    url(r'^nuevo$', AltaExamen.as_view(), name='nuevo_examen'),
    url(r'^borrar/(?P<pk>\d+)$', BajaExamen.as_view(), name='borrar_examen'),
]
