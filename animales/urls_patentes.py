from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_patente, name='lista_patentes'),    
    url(r'^nueva$', alta_patente, name='nueva_patente'),
    url(r'^imprimir/(?P<pk>\d+)$', PdfCarnet.as_view(), name='carnet_pdf'),
    url(r'^borrar/(?P<pk>\d+)$', baja_patente, name='borrar_patente'),
    url(r'^editar/(?P<pk>\d+)$', modificacion_patente, name='modificar_patente'),
    url(r'^detalles/(?P<pk>\d+)$', DetallePatente.as_view(), name='detalle_patente'),
    url(r'^beneficios/garrapaticida/(?P<pk>\d+)$', retiro_garrapaticida, name='retiro_garrapaticida'),
    url(r'^beneficios/antiparasitario/(?P<pk>\d+)$', retiro_antiparasitario, name='retiro_antiparasitario'),
]
