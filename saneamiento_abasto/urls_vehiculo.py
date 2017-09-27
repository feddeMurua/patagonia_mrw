from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_vehiculo, name='lista_vehiculos'),
    url(r'^(?P<pk>\d+)$', DetalleVehiculo.as_view(), name='detalle_vehiculo'),
    url(r'^nuevo_vehiculo$', AltaVehiculo.as_view(), name='nuevo_vehiculo'),
    url(r'^borrar/(?P<pk>\d+)$', BajaVehiculo.as_view(), name='borrar_vehiculo'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionVehiculo.as_view(), name='modificar_vehiculo'),
    url(r'^nroDisposicion/(?P<pk>\d+)/(?P<nro_disp>\w+)$', ingresar_disposicion, name='ingresar_disposicion'),
]
