from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_reinspeccion, name='lista_reinspecciones'),
    url(r'^nueva$', alta_reinspeccion, name='nueva_reinspeccion'),
    url(r'^nueva/agregar_producto$', agregar_producto, name='agregar_producto'),
    url(r'^nueva/eliminar_producto/(?P<nombre>\w+)$', eliminar_producto, name='eliminar_producto'),
    url(r'^productos/nuevo$', AltaProducto.as_view(), name='alta_producto'),
    url(r'^precios$', precios_reinspeccion, name='precios_reinspeccion')
]
