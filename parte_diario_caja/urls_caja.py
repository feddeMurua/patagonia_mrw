from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_movimientos, name='lista_movimientos'),
    url(r'^pdf/(?P<anio>\d+)/(?P<mes>\d+)/(?P<dia>\d+)/$', pdf_parte_diario, name='parte_diario_pdf'),
    url(r'^detalle/(?P<pk>\d+)$', detalle_movimiento, name='detalle_movimiento'),
    url(r'^verificar_nro_ingreso/$', verificar_nro_ingreso, name='verificar_nro_ingreso'),
]
