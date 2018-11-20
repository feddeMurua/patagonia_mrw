from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_libreta, name='lista_libretas'),
    url(r'^pdf_libreta/(?P<pk>\d+)$', PdfLibreta.as_view(), name='pdf_libreta'),
    url(r'^pdf_solicitud/(?P<pk>\d+)$', PdfSolicitud.as_view(), name='pdf_solicitud'),
    url(r'^pdf_renovacion/(?P<pk>\d+)$', PdfRenovacion.as_view(), name='pdf_renovacion'),
    url(r'^nueva$', alta_libreta, name='nueva_libreta'),
    url(r'^borrar/(?P<pk>\d+)$', baja_libreta, name='borrar_libreta'),
    url(r'^editar/(?P<pk>\d+)$', modificacion_libreta, name='modificar_libreta'),
    url(r'^(?P<pk>\d+)$', DetalleLibreta.as_view(), name='detalle_libreta'),
    url(r'^renovacion/(?P<pk>\d+)$', renovacion_libreta, name='renovacion_libreta')
]
