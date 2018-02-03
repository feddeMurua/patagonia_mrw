from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_vehiculo, name='lista_vehiculos'),
    url(r'^(?P<pk>\d+)$', DetalleVehiculo.as_view(), name='detalle_vehiculo'),
    url(r'^nuevo_vehiculo$', alta_vehiculo, name='nuevo_vehiculo'),
    url(r'^borrar/(?P<pk>\d+)$', baja_vehiculo, name='borrar_vehiculo'),
    url(r'^editar/(?P<pk>\d+)$', modificacion_vehiculo, name='modificar_vehiculo'),
    url(r'^pdf/(?P<pk>\d+)$', PdfVehiculo.as_view(), name='vehiculo_pdf'),
    url(r'^getRubros/(?P<id_categoria>\w+)$', get_rubros_json, name='get_rubros')
]
