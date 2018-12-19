from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_cc, name='lista_cc'),
    url(r'^(?P<pk>\d+)/periodos$', periodos_cc, name='periodos_cc'),
    url(r'^(?P<pk>\d+)/periodo/(?P<mes>\d+)/(?P<anio>\d+)/detalle$', detalle_periodo, name='detalle_periodo'),
    url(r'^cancelar/(?P<pk>\d+)$', cancelar_deuda_cc, name='cancelar_deuda_cc'),
    url(r'^pdf/(?P<pk>\d+)/(?P<mes>\d+)/(?P<anio>\d+)$', pdf_certificado, name='pdf_certificado'),
]
