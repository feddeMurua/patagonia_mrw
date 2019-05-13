from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_reinspeccion, name='lista_reinspecciones'),
    url(r'^nueva$', alta_reinspeccion, name='nueva_reinspeccion'),
    url(r'^calculo_importe/(?P<kg>\w+)$', calculo_importe_json, name='calculo_importe'),
    url(r'^nueva_cc$', alta_reinspeccion_cc, name='nueva_reinspeccion_cc'),
    url(r'^modificar/(?P<pk>\d+)/(?P<periodo_pk>\d+)$', modificar_reinspeccion, name='modificar_reinspeccion'),
    url(r'^borrar/(?P<pk>\d+)$', baja_reinspeccion, name='baja_reinspeccion'),
    url(r'^calculo_kg_importe$', calculo_kg_importe, name='calculo_kg_importe'),
    url(r'^agregar_producto$', agregar_producto, name='agregar_producto'),
    url(r'^agregar_producto_reinspeccion/(?P<reinspeccion_pk>\d+)/(?P<periodo_pk>\d+)$', agregar_producto_reinspeccion,
        name='agregar_producto_reinspeccion'),
    url(r'^eliminar_producto/(?P<nombre>\[\w|\W]+)$', eliminar_producto, name='eliminar_producto'),
    url(r'^modificar_producto/(?P<nombre>\[\w|\W]+)/(?P<kg>\w+)$', modificar_producto, name='modificar_producto'),
    url(r'^modificar_producto_reinspeccion/(?P<pk>\d+)/(?P<nombre>[\w|\W]+)/(?P<kg>\w+)$', modificar_producto_reinspeccion,
        name='modificar_producto_reinspeccion'),
    url(r'^productos/nuevo$', AltaProducto.as_view(), name='alta_producto'),
    url(r'^carga_productos/(?P<reinspeccion_pk>\d+)$', carga_productos, name='carga_productos'),
    url(r'^productos/(?P<reinspeccion_pk>\d+)/(?P<periodo_pk>\d+)$', lista_productos, name='lista_productos'),
    url(r'^productos/(?P<pk>\d+)/borrar$', borrar_producto, name='borrar_producto'),
    url(r'^precios$', precios_reinspeccion, name='precios_reinspeccion')
]
