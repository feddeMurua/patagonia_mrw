from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_esterilizaciones, name='lista_esterilizaciones'),
    url(r'^nuevo$', AltaEsterilizacion.as_view(), name='nueva_esterilizacion'),  
    #url(r'^borrar/(?P<pk>\d+)$', BajaAnalisis.as_view(), name='borrar_analisis'),
    #url(r'^(?P<pk>\d+)$', DetalleAnalisis.as_view(), name='detalle_analisis'),
 ]
