from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_reinspeccion, name='lista_reinspecciones'),
    url(r'^nueva$', AltaReinspeccion.as_view(), name='nueva_reinspeccion'),
    url(r'^borrar/(?P<pk>\d+)$', BajaReinspeccion.as_view(), name='borrar_reinspeccion'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionReinspeccion.as_view(), name='modificar_reinspeccion'),
]
