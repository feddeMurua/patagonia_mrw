from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_libreta, name='lista_libretas'),
    url(r'^nueva$', alta_libreta, name='nueva_libreta'),
    url(r'^pdf_libreta/(?P<pk>\d+)$', pdf_libreta, name='pdf_libreta'),
    url(r'^borrar/(?P<pk>\d+)$', baja_libreta, name='borrar_libreta'),
    url(r'^editar/(?P<pk>\d+)$', modificacion_libreta, name='modificar_libreta'),
    url(r'^confirmar/(?P<pk>\d+)$', confirmar_libreta, name='confirmar_libreta'),
    url(r'^pdf_libreta/(?P<pk>\d+)$', pdf_libreta, name='pdf_libreta'),
    url(r'^pdf_formulario/(?P<pk>\d+)$', pdf_formulario, name='pdf_formulario'),
    url(r'^detalle/(?P<pk>\d+)$', DetalleLibreta.as_view(), name='detalle_libreta'),
    url(r'^renovacion/(?P<pk>\d+)$', renovar_libreta, name='renovar_libreta'),
    url(r'^confirmar_renovacion/(?P<pk>\d+)$', confirmar_renovacion, name='confirmar_renovacion'),
]
