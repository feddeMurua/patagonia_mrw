from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_retiro_entrega, name='lista_retiro_entrega'),
    url(r'^nuevo$', AltaRetiroEntrega.as_view(), name='nuevo__retiro_entrega'),
]
