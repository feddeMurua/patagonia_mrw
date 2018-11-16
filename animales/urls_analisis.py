from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_analisis, name='lista_analisis'),
    url(r'^nuevo$', alta_analisis, name='nuevo_analisis'),
    url(r'^agregar_porcino$', agregar_porcino, name='agregar_porcino'),
    url(r'^eliminar_porcino/(?P<precinto>\d+)$', eliminar_porcino, name='eliminar_porcino'),
    url(r'^borrar/(?P<pk>\d+)$', baja_analisis, name='borrar_analisis'),
    url(r'^editar/(?P<pk>\d+)$', modificacion_analisis, name='modificacion_analisis'),
    url(r'^resultado/(?P<pk>\d+)$', resultado_analisis, name='resultado_analisis'),
    url(r'^detalle/(?P<pk>\d+)$', detalle_analisis, name='detalle_analisis'),
    url(r'^pdf/(?P<pk>\d+)$', PdfAnalisis.as_view(), name='pdf_analisis')
]
