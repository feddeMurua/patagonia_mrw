from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_movimientos, name='lista_movimientos'),
    url(r'^get_movimientos/(?P<term>\w+)$', get_movimientos, name='get_movimientos'),
    url(r'^pdf/(?P<anio>\d+)/(?P<mes>\d+)/(?P<dia>\d+)/$', pdf_parte_diario, name='parte_diario_pdf'),
    url(r'^detalle/(?P<pk>\d+)$', detalle_movimiento, name='detalle_movimiento'),
    url(r'^modificar_movimiento/(?P<pk>\d+)$', modificar_movimiento, name='modificar_movimiento'),
    url(r'^modificar_detalle/(?P<pk>\d+)$', modificar_detalle, name='modificar_detalle'),
    url(r'^verificar_nro_ingreso/$', verificar_nro_ingreso, name='verificar_nro_ingreso'),
]
