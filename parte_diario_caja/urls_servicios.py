from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_servicios, name='lista_servicios'),
    url(r'^nuevo$', alta_servicio, name='nuevo_servicio'),
    url(r'^borrar/(?P<pk>\d+)$', baja_servicio, name='borrar_servicio'),
    url(r'^editar/(?P<pk>\d+)$', modificacion_servicio, name='modificar_servicio'),
]
