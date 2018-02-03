from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_movimientos, name='lista_movimientos'),
    url(r'^pdf$', PdfParteDiario.as_view(), name='parte_diario_pdf'),
    url(r'^detalle/(?P<pk>\d+)$', detalle_movimiento, name='detalle_movimiento')
]
