from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^(?P<pk_vehiculo>\w+)$', lista_desinfecciones, name='lista_desinfecciones'),
    url(r'^nueva/(?P<pk_vehiculo>\d+)$', nueva_desinfeccion, name='nueva_desinfeccion'),
    url(r'^borrar/(?P<pk>\d+)$', baja_desinfeccion, name='borrar_desinfeccion'),
    url(r'^editar/(?P<pk_vehiculo>\d+)/(?P<pk>\d+)$', modificar_desinfeccion, name='modificar_desinfeccion')
]
