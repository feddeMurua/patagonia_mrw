from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_reinspeccion, name='lista_reinspecciones'),
    url(r'^nueva$', alta_reinspeccion, name='nueva_reinspeccion'),
    url(r'^borrar/(?P<reinspeccion_pk>\d+)$', baja_reinspeccion, name='borrar_reinspeccion'),
    url(r'^editar/(?P<reinspeccion_pk>\d+)$', modificacion_reinspeccion, name='modificar_reinspeccion'),
    url(r'^productos/(?P<reinspeccion_pk>\d+)$', lista_productos, name='lista_productos'),
    url(r'^productos/nuevo/(?P<reinspeccion_pk>\d+)$', nuevo_producto, name='nuevo_item'),
    url(r'^productos/nuevo$', AltaProducto.as_view(), name='nuevo_producto'),
    url(r'^productos/borrar/(?P<pk>\d+)$', baja_producto, name='borrar_producto'),
    url(r'^productos/editar/(?P<pk>\d+)/(?P<reinspeccion_pk>\d+)$', modificar_producto, name='modificar_producto'),
]
