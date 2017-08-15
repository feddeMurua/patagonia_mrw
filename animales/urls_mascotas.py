from django.conf.urls import url
from .views import *

urlpatterns = [
    #url(r'^$', lista_mascotas, name='lista_mascotas'),
    url(r'^nuevo$', AltaMascota.as_view(), name='nuevo_mascota'),  
    url(r'^borrar/(?P<pk>\d+)$', BajaMascota.as_view(), name='borrar_mascota'),
    url(r'^editar/(?P<pk>\d+)$', ModificacionMascota.as_view(), name='modificar_mascota'),
    url(r'^(?P<pk>\d+)$', DetalleMascota.as_view(), name='detalle_mascota'),
 ]