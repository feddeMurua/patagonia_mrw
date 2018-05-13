from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_controles, name='lista_controles'),
    url(r'^nuevo$', alta_control, name='nuevo_control'),
    url(r'^borrar/(?P<pk>\d+)$', baja_control, name='borrar_control'),
    url(r'^visitas/(?P<pk_control>\d+)$', lista_visitas_control, name='lista_visitas'),
    url(r'^visitas/nueva/(?P<pk_control>\d+)$', alta_visita, name='nueva_visita'),
    url(r'^visitas/borrar/(?P<pk>\d+)$', baja_visita, name='borrar_visita'),
    url(r'^visitas/modificar/(?P<pk>\d+)/(?P<pk_control>\d+)$', modificacion_visita,
        name='modificar_observacion_visita'),
]
