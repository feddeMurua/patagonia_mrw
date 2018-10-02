from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_reinspeccion, name='lista_reinspecciones'),
    url(r'^nueva$', alta_reinspeccion, name='nueva_reinspeccion'),
    url(r'^calculo_importe/(?P<kg>\w+)$', calculo_importe_json, name='calculo_importe'),
    url(r'^nueva_cc$', alta_reinspeccion_cc, name='nueva_reinspeccion_cc'),
    url(r'^calculo_kg_importe$', calculo_kg_importe, name='calculo_kg_importe'),
    url(r'^agregar_producto$', agregar_producto, name='agregar_producto'),
    url(r'^eliminar_producto/(?P<nombre>\w+)$', eliminar_producto, name='eliminar_producto'),
    url(r'^modificar_producto/(?P<nombre>\w+)/(?P<kg>\w+)$', modificar_producto, name='modificar_producto'),
    url(r'^modificar_producto_reinspeccion/(?P<pk>\d+)/(?P<nombre>\w+)/(?P<kg>\w+)$', modificar_producto_reinspeccion,
        name='modificar_producto_reinspeccion'),
    url(r'^productos/nuevo$', AltaProducto.as_view(), name='alta_producto'),
    url(r'^carga_productos/(?P<reinspeccion_pk>\d+)$', carga_productos, name='carga_productos'),
    url(r'^productos/(?P<reinspeccion_pk>\d+)/(?P<pagado>\d+)$', lista_productos, name='lista_productos'),
    url(r'^precios$', precios_reinspeccion, name='precios_reinspeccion')
]
