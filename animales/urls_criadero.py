from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_solicitudes, name='lista_solicitudes'),
    url(r'^nueva_solicitud$', alta_solicitud, name='nueva_solicitud'),
    url(r'^borrar_solicitud/(?P<pk>\d+)$', baja_solicitud, name='borrar_solicitud'),
    url(r'^detalle_solicitud/(?P<pk>\d+)$', detalles_solicitud, name='detalle_solicitud'),
    url(r'^aplazo_solicitud/(?P<pk>\d+)$', aplazo_solicitud, name='aplazo_solicitud'),
    url(r'^pdf_solicitud/(?P<pk>\d+)$', PdfSolicitud.as_view(), name='pdf_solicitud'),
    url(r'^disposicion/(?P<pk>\d+)$', alta_disposicion, name='nueva_disposicion')
]
