from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_tsa, name='lista_tsa'),
    url(r'^nuevo_tsa$', AltaTsa.as_view(), name='nuevo_tsa'),
    url(r'^borrar/(?P<pk>\d+)$', BajaTsa.as_view(), name='borrar_tsa'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionTsa.as_view(), name='modificar_tsa'),
]
