from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_abastecedor, name='lista_abastecedores'),
    url(r'^alta$', alta_abastecedor, name='alta_abastecedor'),
    url(r'^nuevo/particular$', nuevo_abastecedor_particular, name='nuevo_abastecedor_particular'),
    url(r'^nuevo/empresa$', nuevo_abastecedor_empresa, name='nuevo_abastecedor_empresa'),
    url(r'^borrar/(?P<pk>\d+)$', baja_abastecedor, name='borrar_abastecedor'),
]
