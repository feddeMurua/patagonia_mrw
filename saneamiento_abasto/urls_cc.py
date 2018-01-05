from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_cc, name='lista_cc'),
    url(r'^pagos/(?P<pk>\d+)$', pagos_cc, name='pagos_cc'),
    url(r'^realizar_pago/(?P<pk>\d+)$', realizar_pago_cc, name='realizar_pago_cc'),
    url(r'^detalle/(?P<pk>\d+)$', detalle_cc, name='detalle_cc')
]
