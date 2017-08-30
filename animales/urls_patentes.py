from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_patente, name='lista_patentes'),    
    url(r'^nueva$', alta_patente, name='nueva_patente'),
    url(r'^imprimir/(?P<pk>\d+)$', PdfCarnet.as_view(), name='carnet_pdf'),
    url(r'^borrar/(?P<pk>\d+)$', BajaPatente.as_view(), name='borrar_patente'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionPatente.as_view(), name='modificar_patente'),
]
