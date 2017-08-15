from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_persona, name='lista_personas'),
    url(r'^(?P<id_persona>\d+)$', lista_detalles_persona, name='detalle_persona'),
    url(r'^nueva$', AltaPersona.as_view(), name='nueva_persona'),
    url(r'^borrar/(?P<pk>\d+)$', BajaPersona.as_view(), name='borrar_persona'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionPersona.as_view(), name='modificar_persona')
]