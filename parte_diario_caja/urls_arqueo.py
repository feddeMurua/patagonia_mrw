from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_arqueos, name='lista_arqueos'),
    url(r'^nuevo$', alta_arqueo, name='nuevo_arqueo'),
    url(r'^get_iv/(?P<turno>\w+)$', get_iv, name='get_iv'),
    url(r'^detalle/(?P<pk>\d+)$', detalle_arqueo, name='detalle_arqueo'),
    url(r'^pdf/(?P<planilla>\d+)$', pdf_arqueo, name='arqueo_pdf')
]
