from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_retiro_entrega, name='lista_retiro_entrega'),
    url(r'^nuevo$', alta_retiro_etrega, name='nuevo_retiro_entrega'),
    url(r'^getMascotas/(?P<pk_interesado>\d+)/$', get_mascotas, name="get_mascotas"),
]
