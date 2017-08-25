from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_abastecedor, name='lista_abastecedores'),
    url(r'^nuevo$', AltaAbastecedor.as_view(), name='nuevo_abastecedor'),   
]
