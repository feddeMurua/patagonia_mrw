from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_controles, name='lista_controles'),
    url(r'^nuevo$', alta_control, name='nuevo_control'),
    #url(r'^borrar/(?P<pk>\d+)$', BajaPatente.as_view(), name='borrar_patente'),
    #url(r'^editar/(?P<pk>\d+)$', ModificacionPatente.as_view(), name='modificar_patente'),
]
