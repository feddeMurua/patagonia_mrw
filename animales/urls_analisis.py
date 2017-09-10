from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_analisis, name='lista_analisis'),
    url(r'^nuevo$', alta_analisis, name='nuevo_analisis'),
    url(r'^borrar/(?P<pk>\d+)$', baja_analisis, name='borrar_analisis'),
    url(r'^(?P<pk>\d+)$', detalle_analisis, name='detalle_analisis'),
]
