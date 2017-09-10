from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_libreta, name='lista_libretas'),
    url(r'^(?P<pk>\d+)$', DetalleLibreta.as_view(), name='detalle_libreta'),
    url(r'^nueva$', AltaLibreta.as_view(), name='nueva_libreta'),
    url(r'^borrar/(?P<pk>\d+)$', baja_libreta, name='borrar_libreta'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionLibreta.as_view(), name='modificar_libreta'),
]
