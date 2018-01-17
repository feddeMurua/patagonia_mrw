from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_controles_plaga, name='lista_controles_plagas'),
    url(r'^(?P<pk>\d+)$', DetalleControlPlaga.as_view(), name='detalle_control_plaga'),
    url(r'^nuevo$', alta_control_plaga, name='nuevo_control_plaga'),
    url(r'^borrar/(?P<pk>\d+)$', baja_control_plaga, name='borrar_control_plaga'),
    url(r'^editar/(?P<pk>\d+)$', modificacion_control_plaga, name='modificar_control_plaga'),
    url(r'^pago_diferido/(?P<pk>\d+)$', pago_diferido, name='pago_diferido')
]
