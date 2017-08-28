from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_solicitudes, name='lista_solicitudes'),
    url(r'^nuevo$', alta_solicitud, name='nueva_solicitud'),
    url(r'^borrar/(?P<pk>\d+)$', BajaSolicitud.as_view(), name='borrar_solicitud'),
    url(r'^detalle/(?P<pk>\d+)$', detalles_solicitud, name='detalle_solicitud'),
    url(r'^aplazo/(?P<pk>\d+)$', aplazo_solicitud, name='aplazo_solicitud'),
    url(r'^pdf/(?P<pk>\d+)$', PdfSolicitud.as_view(), name='pdf_solicitud')
]
