from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_abastecedor, name='lista_abastecedores'),
    url(r'^alta$', alta_abastecedor, name='alta_abastecedor'),
    url(r'^alta/informacionAdicional/(?P<pk>\d+)$', info_adicional_abastecedor, name='info_adicional_abastecedor'),
    url(r'^nuevo$', nuevo_abastecedor, name='nuevo_abastecedor'),
    url(r'^borrar/(?P<pk>\d+)$', BajaAbastecedor.as_view(), name='borrar_abastecedor'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionAbastecedor.as_view(), name='modificar_abastecedor'),
]
