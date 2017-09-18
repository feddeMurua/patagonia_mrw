from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_controles_plaga, name='lista_controles_plagas'),
    url(r'^(?P<pk>\d+)$', DetalleControlPlaga.as_view(), name='detalle_control_plaga'),
    url(r'^nuevo$', AltaControlPlaga.as_view(), name='nuevo_control_plaga'),
    url(r'^borrar/(?P<pk>\d+)$', BajaControlPlaga.as_view(), name='borrar_control_plaga'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionControlPlaga.as_view(), name='modificar_control_plaga'),

]
