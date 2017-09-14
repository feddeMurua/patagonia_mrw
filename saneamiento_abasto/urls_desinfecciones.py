from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_desinfecciones, name='lista_desinfecciones'),
    url(r'^nueva_desinfeccion$', AltaDesinfeccion.as_view(), name='nueva_desinfeccion'),
    url(r'^borrar/(?P<pk>\d+)$', BajaDesinfeccion.as_view(), name='borrar_desinfeccion'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionDesinfeccion.as_view(), name='modificar_desinfeccion'),
]
