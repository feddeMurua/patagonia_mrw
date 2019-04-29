from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_cc, name='lista_cc'),
    url(r'^(?P<pk>\d+)/periodos$', periodos_cc, name='periodos_cc'),
    url(r'^periodo/(?P<pk>\d+)/detalle$', detalle_periodo, name='detalle_periodo'),
    url(r'^periodo/(?P<pk>\d+)/certificado$', certificado_deuda, name='certificado_deuda'),
    url(r'^periodo/(?P<pk>\d+)/certificado/abonar$', abonar_certificado, name='abonar_certificado'),
    url(r'^pdf/(?P<pk>\d+)$', pdf_certificado, name='pdf_certificado'),
]
