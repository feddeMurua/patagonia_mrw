from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_tpp, name='lista_tpp'),
    url(r'^nuevo_tpp$', AltaTpp.as_view(), name='nuevo_tpp'),
    url(r'^borrar/(?P<pk>\d+)$', BajaTpp.as_view(), name='borrar_tpp'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionTpp.as_view(), name='modificar_tpp'),
]
