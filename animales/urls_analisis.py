from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_analisis, name='lista_analisis'),
    url(r'^nuevo$', AltaAnalisis.as_view(), name='nuevo_analisis'),  
    url(r'^borrar/(?P<pk>\d+)$', BajaAnalisis.as_view(), name='borrar_analisis'),
    url(r'^(?P<pk>\d+)$', DetalleAnalisis.as_view(), name='detalle_analisis'),
 ]
