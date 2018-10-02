from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_retiro_entrega, name='lista_retiro_entrega'),
    url(r'^nuevo$', alta_tramite, name='nuevo_tramite'),
    url(r'^editar/(?P<pk>\d+)$', modificacion_tramite, name='modificar_tramite')
]
