from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_vehiculo, name='lista_vehiculos'),
    url(r'^(?P<pk>\d+)$', DetalleVehiculo.as_view(), name='detalle_vehiculo'),
    url(r'^nuevo_vehiculo$', alta_vehiculo, name='nuevo_vehiculo'),
    url(r'^borrar/(?P<pk>\d+)$', baja_vehiculo, name='borrar_vehiculo'),
    url(r'^editar/(?P<pk>\d+)$', modificacion_vehiculo, name='modificar_vehiculo'),
    url(r'^pdf/(?P<nro>\d+)$', pdf_vehiculo, name='vehiculo_pdf'),
    url(r'^getRubros/(?P<id_categoria>\[\w|\W]+)$', get_rubros_json, name='get_rubros'),
    url(r'^nueva_marca$', AltaMarca.as_view(), name='alta_marca'),
    url(r'^nuevo_modelo$', AltaModelo.as_view(), name='alta_modelo')
]
