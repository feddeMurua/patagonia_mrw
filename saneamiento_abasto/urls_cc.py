from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_cc, name='lista_cc'),
    url(r'^(?P<pk>\d+)/periodos$', periodos_cc, name='periodos_cc'),
    url(r'^periodo/(?P<pk>\d+)/detalle$', detalle_periodo, name='detalle_periodo'),
    url(r'^cancelar/(?P<pk>\d+)$', cancelar_deuda_cc, name='cancelar_deuda_cc'),
    url(r'^pdf/(?P<pk>\d+)$', pdf_certificado, name='pdf_certificado'),
]
