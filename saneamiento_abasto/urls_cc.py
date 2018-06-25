from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_cc, name='lista_cc'),
    url(r'^detalle/(?P<pk>\d+)$', detalle_cc, name='detalle_cc'),
    url(r'^cancelar/(?P<pk>\d+)$', cancelar_deuda_cc, name='cancelar_deuda_cc'),
    url(r'^pdf/(?P<pk>\d+)/(?P<mes>\d+)/(?P<anio>\d+)$', PdfCertificado.as_view(), name='pdf_certificado'),
]
