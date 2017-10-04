from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^(?P<pk_vehiculo>\d+)$', lista_desinfecciones, name='lista_desinfecciones'),
    url(r'^nueva/(?P<pk_vehiculo>\d+)$', nueva_desinfeccion, name='nueva_desinfeccion'),
    url(r'^borrar/(?P<pk>\d+)$', baja_desinfeccion, name='borrar_desinfeccion'),
    url(r'^editar/(?P<pk_vehiculo>\d+)/(?P<pk>\d+)$', ModificacionDesinfeccion.as_view(),
        name='modificar_desinfeccion'),
]
