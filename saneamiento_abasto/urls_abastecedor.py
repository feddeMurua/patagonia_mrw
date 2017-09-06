from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_abastecedor, name='lista_abastecedores'),
    url(r'^nuevo$', AltaAbastecedor.as_view(), name='nuevo_abastecedor'),
    url(r'^borrar/(?P<pk>\d+)$', BajaAbastecedor.as_view(), name='borrar_abastecedor'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionAbastecedor.as_view(), name='modificar_abastecedor'),
]
