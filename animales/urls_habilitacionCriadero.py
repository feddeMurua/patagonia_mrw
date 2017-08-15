from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_habilitaciones, name='lista_habilitaciones'),
    url(r'^nuevo$', AltaHabilitacion.as_view(), name='nueva_habilitacion'),  
    #url(r'^borrar/(?P<pk>\d+)$', BajaAnalisis.as_view(), name='borrar_analisis'),
    #url(r'^(?P<pk>\d+)$', DetalleAnalisis.as_view(), name='detalle_analisis'),
 ]
