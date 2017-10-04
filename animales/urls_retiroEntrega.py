from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', lista_retiro_entrega, name='lista_retiro_entrega'),
    url(r'^nuevo$', alta_tramite, name='nuevo_tramite'),
    url(r'^nuevo/patentado$', alta_tramite_patentado, name='nuevo_tramite_patentado'),
    url(r'^nuevo/nopatentado$', alta_tramite_nopatentado, name='nuevo_tramite_nopatentado'),
]
